# Pipeline GeoJSON sang PostGIS

Đọc dữ liệu ranh giới GeoJSON, nạp vào PostGIS, chuyển tọa độ sang EPSG:32648, tính diện tích và xuất ra CSV.

## Chạy dự án

Mở Docker Desktop và chạy lệnh sau trong thư mục dự án:

```bash
docker compose up --build
```

Kết quả được lưu tại `output/stats.csv`, gồm 5.166 dòng dữ liệu.

Container `app` kết thúc với mã `0` sau khi xử lý và kiểm thử thành công; cơ sở dữ liệu vẫn chạy.

Chi tiết cập nhật: [CHANGELOG.md](CHANGELOG.md).
