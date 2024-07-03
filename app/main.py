from fastapi import FastAPI
from app.routes import router
from app.infrastructure.db import init_db


app = FastAPI(
    title="Desarrollo de APIs con Python",
    description="Proyecto con fastapi y demás",
    version="1.0",
    docs_url="/",
    redoc_url=None
)
app.include_router(router)


# @app.on_event("startup")
# def on_startup():
#     init_db()
