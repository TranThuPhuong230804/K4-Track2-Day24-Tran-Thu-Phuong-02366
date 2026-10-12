# Token giả trong lịch sử — Trần Thu Phương (02366)

- Scanner: Gitleaks **8.30.1**, cấu hình `.gitleaks.toml`, rule `lab24-synthetic-token`.
- `gitleaks git --config .gitleaks.toml --redact --verbose .` tìm **1 finding** tại `lab-fake-secret.txt:1`, commit `1bdd849922156c868a5ee9293d68f5b72e242d2c`; exit code 1 như checkpoint dự kiến. Token là `LAB24-DEMO` vô hiệu được cài sẵn cho bài lab.
- `gitleaks dir --config .gitleaks.toml --redact .` quét cây làm việc, không có finding (exit code 0). `.gitleaks.toml` bỏ qua `.venv/` trong phép quét này vì đó là môi trường Python cục bộ, không thuộc bài nộp.
- `.pre-commit-config.yaml` pin hook `gitleaks-system` ở `v8.30.1`; `requirements.lock` chứa hash cho từng dependency và lệnh cài `--require-hashes` chạy được.

Nếu đây là credential thật: thu hồi hoặc rotate ngay, rà log sử dụng để xác định ảnh hưởng và xử lý hệ thống liên quan. Xoá file khỏi HEAD không vô hiệu hoá credential đã lộ trong lịch sử. Pin dependency và hook giúp kiểm soát các thay đổi sau này, không thay thế việc rotate.
