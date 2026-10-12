Đối chiếu các kiểm soát trong bài lab

Với Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15 tại https://vanban.chinhphu.vn/?docid=214590&pageid=27160 thì agent/pii.py cho thấy cách nhận diện và che PII còn agent/policy.py cùng reports/attack-after.log cho thấy việc giới hạn đọc và gửi dữ liệu

Với Nghị định 356/2025/NĐ-CP tại https://vanban.chinhphu.vn/?docid=216387&pageid=27160&typegroupid=4 thì agent/ledger.py và reports/ledger.jsonl là bằng chứng mỗi quyết định công cụ có lý do và hash để phát hiện sửa đổi

Với Luật Trí tuệ nhân tạo số 134/2025/QH15 tại https://vanban.chinhphu.vn/?docid=216334&pageid=27160 thì agent/runner.py và tests/test_split.py cho thấy hai run được tách ra và quyền được kiểm trước khi đọc hồ sơ

Với OWASP ASI01 ASI03 và ASI04 tại https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/ thì agent/runner.py và agent/policy.py liên quan đến chặn chỉ thị chèn vào cùng giới hạn quyền còn .pre-commit-config.yaml requirements.lock và reports/secrets-incident.md là bằng chứng kiểm tra nguồn cung ứng

Các đối chiếu trên chỉ mô tả control của bài lab Điều khoản pháp lý cụ thể chưa xác minh và kết quả chạy mock với dữ liệu giả không chứng minh hệ thống thật đã tuân thủ pháp luật
