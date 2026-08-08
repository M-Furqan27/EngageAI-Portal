"""
backend/core/database.py

SQLAlchemy engine, session, aur Base — sab 9 modules ke models.py
isi Base se inherit karenge (Base.metadata sab tables track karta hai).
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

# pool_pre_ping: har checkout se pehle connection "ping" karta hai — agar
# Neon ne idle connection band kar di ho (SSL connection closed) to naya
# connection le leta hai, error nahi deta.
# pool_recycle: 5 min se purane connections ko khud hi recycle kar deta hai,
# taake serverless Postgres (Neon) ke idle-timeout se pehle hi refresh ho jayein.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
)
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