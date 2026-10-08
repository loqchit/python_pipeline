import os
import geopandas as gpd
import pandas as pd
from sqlalchemy import create_engine, text

def main():
    host = os.environ.get('DB_HOST', 'localhost')
    user = os.environ.get('DB_USER', 'user')
    password = os.environ.get('DB_PASS', 'password')
    dbname = os.environ.get('DB_NAME', 'geodb')
    port = os.environ.get('DB_PORT', '5432')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    
    # Đọc GeoJSON
    gdf = gpd.read_file('data/quangngai_2026_ky18_checked.geojson')
    if gdf.crs is None:
        gdf.set_crs(epsg=4326, inplace=True)
        
    # Nạp vào PostGIS
    gdf.to_postgis('communes', engine, if_exists='replace', index=False, dtype={'geometry': 'Geometry'})
    
    # Chuyển tọa độ (EPSG:32648), tính diện tích và lưu bảng thống kê
    with engine.begin() as conn:
        conn.execute(text("""
            DROP TABLE IF EXISTS commune_stats;
            CREATE TABLE commune_stats AS
            SELECT 
                commune,
                district,
                ST_Transform(geometry, 32648) AS geom_32648,
                ST_Area(ST_Transform(geometry, 32648)) AS area_sqm
            FROM communes;
        """))
        
    # Xuất file CSV
    stats_df = pd.read_sql("SELECT commune, district, area_sqm FROM commune_stats", engine)
    os.makedirs('output', exist_ok=True)
    stats_df.to_csv('output/stats.csv', index=False)

if __name__ == '__main__':
    main()
