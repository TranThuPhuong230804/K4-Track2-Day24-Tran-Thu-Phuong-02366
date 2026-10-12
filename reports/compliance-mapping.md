# Đối chiếu kiểm soát — Trần Thu Phương (02366)

Các tên văn bản và tên nhóm rủi ro OWASP đã được đối chiếu với trang chính thức. **Điều khoản pháp lý cụ thể: chưa xác minh.** Bảng chỉ liên hệ mục tiêu của lab với bằng chứng kỹ thuật, không khẳng định hệ thống thật đã đáp ứng nghĩa vụ pháp luật.

| Nguồn | Liên hệ với bài lab | Bằng chứng trong repo |
|---|---|---|
| [Luật Bảo vệ dữ liệu cá nhân 91/2025/QH15](https://vanban.chinhphu.vn/?docid=214590&pageid=27160) | Hạn chế truy cập và phát tán dữ liệu cá nhân | `agent/pii.py:42`, `agent/policy.py:60`, `reports/attack-after.log` (0 byte) |
| [Nghị định 356/2025/NĐ-CP](https://vanban.chinhphu.vn/?docid=216387&pageid=27160&typegroupid=4) | Ghi lại quyết định xử lý trong mô phỏng | `agent/ledger.py:49`, `reports/ledger.jsonl:1` (reason/hash); `tests/test_ledger.py` |
| [Luật Trí tuệ nhân tạo 134/2025/QH15](https://vanban.chinhphu.vn/?docid=216334&pageid=27160) | Kiểm soát hành vi agent khi dùng dữ liệu và công cụ | `agent/runner.py:94`, `tests/test_obo.py`, `tests/test_split.py` |
| [OWASP ASI01 — Agent Goal Hijack](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Ticket chứa chỉ thị nhằm đổi mục tiêu agent | `corpus/ticket-901.md:5`, `injection-corpus.md`, `reports/attack-before.log:1` |
| [OWASP ASI03 — Identity & Privilege Abuse](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Giới hạn principal và quyền uỷ quyền | `agent/policy.py:68`, `tests/test_obo.py`, `reports/ledger.jsonl:1` (`on_behalf_of`) |
| [OWASP ASI04 — Agentic Supply Chain Vulnerabilities](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | Kiểm secret và dependency | `.gitleaks.toml`, `.pre-commit-config.yaml`, `requirements.lock`, `reports/secrets-incident.md` |

Chỉ có mock, dữ liệu synthetic và sink localhost được kiểm trong bài này. Việc áp dụng văn bản pháp luật vào hệ thống thực cần đối chiếu điều khoản gốc, mục đích xử lý và bối cảnh triển khai.
