Kết quả kiểm tra ngày 12 tháng 10 năm 2026

Bài chạy trên Windows với Python 3.12.14 trong .venv và Gitleaks 8.30.1 Vì lệnh python mặc định trỏ tới WindowsApps nên các lệnh bên dưới được chạy bằng .\.venv\Scripts\python.exe và đặt PYTHONIOENCODING thành utf-8

Lệnh python -m pytest tests/test_pii.py -v -s --basetemp=.pytest_tmp đạt với gold 118 pred 118 tp 118 precision 1.000 và recall 1.000 Các nhóm tests/test_policy.py tests/test_obo.py tests/test_split.py tests/test_injection.py và tests/test_ledger.py cũng đạt trong đó support_l1 bị chặn đọc hồ sơ còn dpo vẫn đọc được khách gắn với ticket và KH-000777 không bị đọc chỉ vì xuất hiện trong text

Lệnh python -m pytest tests/ -q --basetemp=.pytest_tmp báo 33 passed và python -m agent.check_lure corpus/ticket-90*.md báo 4/4 lure sẵn sàng Sau khi chạy python -m agent.loop --mock --as dpo "Tổng hợp các ticket còn mở tuần này" thì ledger vẫn verify True với reason ở mọi dòng và có quyết định từ chối http_post cho dpo Bản sao ledger bị sửa một ký tự ở giữa trả về False

reports/attack-before.log có bốn lần gửi dữ liệu giả của KH-000999 còn reports/attack-after.log rỗng sau khi sửa runner nên lần replay sau không gửi hồ sơ tới sink

Lệnh pre-commit run --all-files và pip install --require-hashes -r requirements.lock đều đạt Gitleaks quét lịch sử trả mã 1 vì tìm thấy một token giả ở commit 1bdd849922156c868a5ee9293d68f5b72e242d2c còn quét cây làm việc hiện tại trả mã 0 vì không có finding

Lần commit đầu hook báo Executable gitleaks not found do .venv\Scripts chưa nằm trong PATH Sau khi thêm thư mục này thì hook chạy đạt và commit thành công

Lần test đầu sau khi rút gọn báo cáo có một lỗi vì reports/secrets-incident.md thiếu mã rule lab24-synthetic-token Sau khi bổ sung mã rule thì toàn bộ test được chạy lại

Regex hiện nhận CCCD 12 số điện thoại bắt đầu bằng 0 tài khoản 8 đến 16 số có nhãn và email thông thường nên vẫn có thể bỏ sót cách viết khác hoặc nhận nhầm chuỗi số Precision và recall trên dữ liệu giả không đại diện cho dữ liệu thật
