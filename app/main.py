from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from app.routers import router
from app.routers_html import router as html_router
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My first FastAPI project",
    description="Author: Vitalii K.",
    version='0.1'
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, tags=['USER part'])
app.include_router(html_router, tags=['Html pages'])


@app.get("/")
def read_root():
    return {'Try': 'go to /docs for more documentation .'}
