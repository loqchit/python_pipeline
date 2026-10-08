import os
import pandas as pd
from sqlalchemy import create_engine, text

def test_pipeline():
    assert os.path.exists('output/stats.csv')
    df = pd.read_csv('output/stats.csv')
    assert len(df) == 5166
    assert 'area_sqm' in df.columns
    
    host = os.environ.get('DB_HOST', 'localhost')
    user = os.environ.get('DB_USER', 'user')
    password = os.environ.get('DB_PASS', 'password')
    dbname = os.environ.get('DB_NAME', 'geodb')
    port = os.environ.get('DB_PORT', '5432')
    
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{dbname}')
    with engine.connect() as conn:
        res = conn.execute(text("SELECT count(*) FROM commune_stats")).scalar()
        assert res == 5166
