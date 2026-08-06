"""
backend/core/database.py

SQLAlchemy engine, session, aur Base — sab 9 modules ke models.py
isi Base se inherit karenge (Base.metadata sab tables track karta hai).
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency — har route mein Depends(get_db) se use hoga.
    Request khatam hone ke baad connection close ho jata hai.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()