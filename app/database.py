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

# print('Hello from database Base')
# print(Base.metadata)
# print(Base.__dict__)
# Dependency
def connect_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    finally:
        db.close()

# async def init_db():
#     """https://habr.com/ru/post/580866/ """
#     async with engine.begin() as conn:
#         # await conn.run_sync(SQLModel.metadata.drop_all)
#         await conn.run_sync(SQLModel.metadata.create_all)