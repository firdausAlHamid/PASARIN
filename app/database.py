from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

# Mengambil URL database dari file .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Membuat 'engine' yang akan mengeksekusi koneksi ke MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Membuat sesi database untuk setiap request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class untuk model-model tabel kita nanti
Base = declarative_base()

# Dependency function untuk digunakan di main.py nanti
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()