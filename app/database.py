from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)

Base = declarative_base()


# Dependency
def connect_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()
