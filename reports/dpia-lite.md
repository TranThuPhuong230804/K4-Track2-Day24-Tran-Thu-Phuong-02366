# DPIA-lite — Trần Thu Phương (02366)

| Mục | Đánh giá trong bài lab |
|---|---|
| Dữ liệu | `corpus/` chứa ticket do bên ngoài viết; `data/customers.json` chứa hồ sơ synthetic có CCCD, STK, điện thoại và email. |
| Mục đích | Tóm tắt ticket; principal `dpo` có thể đọc hồ sơ gắn với ticket cho `support-reply`. |
| Luồng xử lý | Run A đọc ticket, lấy số ticket từ tên file và che PII trước khi tóm tắt (`agent/runner.py:84`–`:92`). Run B dùng `related_tickets` của kho khách hàng để xác định hồ sơ và kiểm quyền trước khi gọi `read_customer` (`agent/runner.py:94`–`:100`). |
| Nơi đi | Sink chỉ nghe `127.0.0.1:10024` (`agent/tools.py:68`). Trước containment có bốn POST trong `reports/attack-before.log`; sau replay không có POST trong `reports/attack-after.log`. |
| Kiểm soát | `agent/policy.py:60` từ chối restricted + egress, kiểm principal, purpose, scope, delegation và TTL. `agent/ledger.py:55` ghi decision/reason với hash chain. |

Giới hạn: `--as` chỉ mô phỏng principal, không xác thực người thật. Regex trong `agent/pii.py` có thể bỏ sót biến thể PII. Tìm kiếm bằng từ khóa có thể trả về nhiều ticket; mapping `related_tickets` có thể đọc nhiều hồ sơ hợp lệ hơn cần thiết. Hash chain chỉ phát hiện sửa trong chuỗi đang còn; nó không tự phát hiện cắt dòng cuối hoặc viết lại toàn bộ chuỗi. Kết quả trên dữ liệu giả không chứng minh tuân thủ pháp luật khi triển khai thật.
