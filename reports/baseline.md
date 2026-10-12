# Baseline — Trần Thu Phương (02366)

1. Chưa có identity riêng cho mỗi run: `agent/loop.py:27` (`_naive_loop`) chỉ nhận `message` và `llm`, không nhận principal hay run ID.
2. Không ai cấp quyền cho `http_post` trong baseline: `agent/loop.py:30` đọc ticket, `agent/loop.py:34` lấy chỉ thị từ nội dung ticket và `agent/loop.py:44` gọi POST trực tiếp, không qua policy. `agent/tools.py:68` chỉ giới hạn đích tới sink localhost; đây không phải kiểm quyền cho người dùng.
3. `reports/attack-before.log:1` đến `:4` là bốn POST chứa record synthetic `KH-000999`, gồm CCCD/STK/điện thoại. Sink ghi body qua `sink/sink.py:58`; script `scripts/replay_evidence.py` gọi riêng `_naive_loop` để tái tạo baseline sau khi runner đã hoàn thiện.
