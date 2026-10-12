Đánh giá tác động dữ liệu

Ticket là dữ liệu nội bộ và có thể chứa chỉ thị do người khác viết Hồ sơ trong data/customers.json là dữ liệu hạn chế vì có CCCD số điện thoại tài khoản và email dù mọi thông tin đều là dữ liệu giả

Run A chỉ đọc ticket rồi lấy số ticket từ tên file và che PII trước khi tóm tắt Run B chỉ nhận số ticket để tìm khách liên quan trong data/customers.json và kiểm quyền trước mỗi lần đọc Vì vậy support_l1 không mở được hồ sơ còn dpo vẫn xử lý được ticket hợp lệ

Khi ticket đòi gửi dữ liệu thì runner kiểm riêng lời gọi http_post với phân loại restricted và egress_enabled=True Ledger ghi lý do từ chối còn reports/attack-after.log rỗng dù reports/attack-before.log có bốn lần gửi trước khi sửa

Kết quả này chỉ đúng trong bài lab dùng dữ liệu giả Tìm kiếm theo từ khóa có thể trả về nhiều hồ sơ hơn cần thiết regex có thể bỏ sót PII và ledger một file không tự phát hiện được việc xóa dòng cuối
