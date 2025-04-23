from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from .models import Base
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
host = os.getenv("MYSQL_HOST")
database = os.getenv("MYSQL_DATABASE")
port = os.getenv("MYSQL_PORT")

DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20,
    connect_args={
        "charset": "utf8mb4",
        "use_unicode": True,
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
