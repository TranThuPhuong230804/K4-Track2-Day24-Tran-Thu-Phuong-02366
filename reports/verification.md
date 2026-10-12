# Kiểm tra bài lab — Trần Thu Phương (02366)

Ngày 12/10/2026, chạy trên Windows với Python 3.11.14 trong `.venv`, pytest 9.1.1 và Gitleaks 8.30.1. Dùng `.venv/Scripts/python.exe` vì interpreter của `.venv` cũ đã trỏ tới đường dẫn không còn hoạt động; `.venv` được sửa bằng `uv venv --allow-existing`.

| Kiểm tra | Kết quả trên repo này |
|---|---|
| `python -m agent.check_lure corpus/ticket-90*.md` | 4/4 lure sẵn sàng |
| `python -m pytest tests/ -q --basetemp=.pytest_tmp` | 33 passed |
| `python -m pytest tests/test_pii.py -s` | 118 gold, 118 pred, 118 TP; precision 1.000, recall 1.000 trên test set synthetic |
| `python -m scripts.replay_evidence` | Baseline 4 POST synthetic; sau containment 0 POST. Ledger 28 dòng, 8 `http_post` deny; `verify()` True; bản sao sửa một dòng cũ trả False. |
| `piptools compile --generate-hashes -o requirements.lock requirements.txt` | Tạo lại lock trên Python 3.11 |
| `pip install --require-hashes -r requirements.lock` | Thành công |
| `gitleaks git --config .gitleaks.toml --redact --verbose .` | 1 finding synthetic ở commit `1bdd849`, exit 1 theo dự kiến |
| `gitleaks dir --config .gitleaks.toml --redact .` | 0 finding, exit 0 sau khi loại `.venv/` khỏi quét cây làm việc |
| `pre-commit run --all-files` | Passed: hook `gitleaks-system` |

`reports/attack-before.log` và `reports/attack-after.log` được tạo lại bằng `scripts/replay_evidence.py` trên sink `127.0.0.1:10024`; file sau rỗng. `reports/ledger.jsonl` được tạo lại từ tám replay có hai principal. Các test dùng sink và ledger riêng, nên log replay không bị lấy nhầm từ pytest.

Nguồn gốc: commit `ba8581b` từng đồng bộ code, lure và báo cáo từ repo tham khảo `hugebenevolence/K4-L3-DAY24-TranDainhan-2A202602642` (commit `3c0303c`). Sau đó bốn control trong `agent/`, ba lure mới và các báo cáo được viết lại theo checkpoint; test và evidence được tạo lại trên phiên bản cuối. Lịch sử Git vẫn ghi việc tham khảo này. Theo `RULES.md`, người nộp cần tự hiểu và giải thích từng control, và không nên trình bày phần đã tham khảo là tự viết độc lập.

Giới hạn còn lại: regex PII mới được đo trên tập giả; `--as` chỉ giả lập quyền; ledger không chống cắt đuôi nếu thiếu mốc tin cậy ngoài file. Windows native không phải môi trường pilot của đề bài, nên kết quả cần đối chiếu thêm trên WSL2/Linux nếu lớp yêu cầu.
