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


_RECOGNIZERS = (
    ("EMAIL", re.compile(r"(?<![\w@])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}(?![\w@])"), 0),
    ("VN_BANK_ACCOUNT", re.compile(
        r"(?:\bSTK\b|số tài khoản)\s*[:#-]?\s*(\d{8,16})(?!\d)", re.I), 1),
    ("VN_CCCD", re.compile(r"(?<!\d)\d{12}(?!\d)"), 0),
    ("VN_PHONE", re.compile(r"(?<!\d)0(?:[ -]?\d){9,10}(?!\d)"), 0),
)


def detect(text: str) -> list[dict]:
    """Return non-overlapping spans, prioritizing explicitly labelled accounts."""
    spans: list[dict] = []
    for kind, pattern, group in _RECOGNIZERS:
        for match in pattern.finditer(text):
            start, end = match.span(group)
            if any(start < prior["end"] and prior["start"] < end for prior in spans):
                continue
            spans.append({"type": kind, "start": start, "end": end})
    spans.sort(key=lambda span: span["start"])
    return spans


def redact(text: str) -> str:
    pieces = []
    cursor = 0
    for entity in detect(text):
        pieces.extend((text[cursor:entity["start"]], f"[REDACTED_{entity['type']}]"))
        cursor = entity["end"]
    pieces.append(text[cursor:])
    return "".join(pieces)
