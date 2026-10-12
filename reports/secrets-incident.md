Ghi nhận token giả trong lịch sử Git

Gitleaks 8.30.1 dùng rule lab24-synthetic-token và tìm thấy một token giả trong lab-fake-secret.txt ở commit 1bdd849922156c868a5ee9293d68f5b72e242d2c Đây là dữ liệu được cài sẵn cho bài lab nên lệnh quét lịch sử trả mã 1 như dự kiến Cây làm việc hiện tại không có finding khi quét lại

Nếu đó là credential thật thì cần thu hồi hoặc rotate ngay rồi xem log sử dụng để xác định ảnh hưởng Xóa file ở commit mới không làm credential cũ mất hiệu lực

Hook gitleaks-system đã được pin trong .pre-commit-config.yaml còn requirements.lock ghi hash cho dependency Các kiểm tra này giúp tránh lặp lại sự cố nhưng không thay thế bước thu hồi khi credential thật bị lộ
