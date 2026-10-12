"""BƯỚC 3a — PII gate TRƯỚC KHI vào context/store (12').

Đọc CHECKPOINTS.md (§3a) trước khi bắt đầu: Presidio không có tiếng Việt
sẵn (AnalyzerEngine() mặc định chỉ hỗ trợ "en"). Đường an toàn cho 2h là
regex recognizer + deny-list cho PERSON — coi spaCy/transformers NER là
stretch goal, KHÔNG bắt buộc.

Interface bắt buộc (tests/test_pii.py gọi trực tiếp 2 hàm này):

    detect(text: str) -> list[dict]
        Mỗi entity: {"type": str, "start": int, "end": int}
        `type` là một trong: "VN_CCCD", "VN_PHONE", "VN_BANK_ACCOUNT", "EMAIL"
        `start`/`end` là offset ký tự trong `text` (offset đầu bao gồm,
        offset cuối KHÔNG bao gồm — giống slice Python text[start:end]).
        Format này khớp với tests/vn_pii_testset.jsonl.

    redact(text: str) -> str
        Trả về `text` sau khi mọi entity từ detect() bị thay bằng
        "[REDACTED_<TYPE>]". Phải xử lý overlap/thứ tự đúng khi có nhiều
        entity (gợi ý: thay từ cuối văn bản về đầu để offset không bị lệch).

Gợi ý định dạng (không bắt buộc đúng regex này, miễn đạt ngưỡng trên test
set ở tests/vn_pii_testset.jsonl):
    VN_CCCD          12 chữ số liên tiếp
    VN_PHONE         0 + 9-10 chữ số, có thể có dấu cách/gạch ngang
    VN_BANK_ACCOUNT  8-16 chữ số liên tiếp, thường đi kèm "STK"/"số tài khoản"
    EMAIL            dạng chuẩn local@domain.tld

Đo bằng: pytest tests/test_pii.py -v -s   (in ra precision/recall)
"""
from __future__ import annotations

import re


_EMAIL = re.compile(r"(?<![\w@])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w@])")
_BANK = re.compile(r"(?i)(?:\bSTK\b|số tài khoản)\s*[:#-]?\s*(\d{8,16})(?!\d)")
_CCCD = re.compile(r"(?<!\d)\d{12}(?!\d)")
_PHONE = re.compile(r"(?<!\d)0\d{9,10}(?!\d)")


def detect(text: str) -> list[dict]:
    found: list[dict] = []
    # Labeled bank numbers take priority over equal-length CCCD/phone matches.
    for kind, pattern in (("EMAIL", _EMAIL), ("VN_BANK_ACCOUNT", _BANK),
                          ("VN_CCCD", _CCCD), ("VN_PHONE", _PHONE)):
        for match in pattern.finditer(text):
            start, end = match.span(1) if kind == "VN_BANK_ACCOUNT" else match.span()
            if any(start < item["end"] and item["start"] < end for item in found):
                continue
            found.append({"type": kind, "start": start, "end": end})
    return sorted(found, key=lambda item: item["start"])


def redact(text: str) -> str:
    for entity in reversed(detect(text)):
        text = (text[:entity["start"]] + f"[REDACTED_{entity['type']}]"
                + text[entity["end"]:])
    return text
