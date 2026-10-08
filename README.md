# GeoJSON to PostGIS Pipeline

Đọc file GeoJSON ranh giới, nạp vào PostGIS, chuyển tọa độ sang EPSG:32648, tính diện tích và xuất ra CSV.

## Chạy dự án

```bash
docker compose up --build
```

Thống kê diện tích sẽ được xuất ra `output/stats.csv`.
