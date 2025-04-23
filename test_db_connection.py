from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import os
from dotenv import load_dotenv

def test_connection():
    load_dotenv()
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    database = os.getenv("MYSQL_DATABASE")
    port = os.getenv("MYSQL_PORT")

    url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

    try:
        engine = create_engine(
            url,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("接続成功！")
            print(f"テストクエリ結果: {result.scalar()}")
    except OperationalError as e:
        print(f"接続エラー: {e}")
        print(f"試行した接続URL: {url}")

if __name__ == "__main__":
    test_connection() 
