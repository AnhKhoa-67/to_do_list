# To-Do List Application (FastAPI)

Ứng dụng quản lý công việc (To-Do List) được xây dựng bằng FastAPI, SQLModel (SQLAlchemy) và SQLite. Dự án này được phát triển theo từng cấp độ yêu cầu.

## Tính năng
- **Xác thực người dùng**: Đăng ký, Đăng nhập sử dụng JWT.
- **Quản lý công việc**: CRUD đầy đủ các tác vụ.
- **Phân quyền**: Người dùng chỉ có thể quản lý công việc của chính mình.
- **Nâng cao**: 
  - Hỗ trợ deadline (hạn chót).
  - Hỗ trợ gắn thẻ (tags) đa dạng.
  - Lọc công việc theo ngày hôm nay và công việc quá hạn.
- **Xóa mềm (Soft Delete)**: Công việc bị xóa sẽ không mất hoàn toàn trong DB (đánh dấu `is_deleted`).
- **Kiểm thử**: Đầy đủ unit tests với `pytest`.
- **Docker**: Hỗ trợ chạy ứng dụng trong container.

## Cài đặt và Chạy

### Cách 1: Chạy trực tiếp
1. Cài đặt các thư viện:
```bash
pip install -r requirements.txt
```
2. Chạy migration để khởi tạo DB:
```bash
alembic upgrade head
```
3. Chạy ứng dụng:
```bash
uvicorn app.main:app --reload
```

### Cách 2: Sử dụng Docker
```bash
docker-compose up --build
```

## API Documentation
Sau khi chạy ứng dụng, bạn có thể truy cập tài liệu API tự động tại:
- Swagger UI: `http://localhost:8000/docs`
- Redoc: `http://localhost:8000/redoc`

## Chạy Kiểm Thử (Tests)
```bash
pytest
```

## Thông tin sinh viên
- **Họ và tên**: Võ Hoàng Anh Khoa
- **MSSV**: 23730551
