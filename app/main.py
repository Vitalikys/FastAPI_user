from typing import Union

from fastapi import FastAPI
from sqlalchemy.orm import declarative_base

from app.routers import router
from app.database import engine, connect_db
from app.database import Base

Base.metadata.create_all(bind=engine)

# def get_application() -> FastAPI:
#     application = FastAPI()
#     application.include_router(router)
#     return application
app = FastAPI(
    title="My first FastAPI project",
    description="Author: Vitalii K.",
    version='0.1'
)
app.include_router(router)

# app = get_application()


@app.get("/")
def read_root():
    return {'Try': 'go to /docs for more documentation .'}


# @app.on_event("startup")
# async def on_startup():
#     await connect_db()