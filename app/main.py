from fastapi import FastAPI
from app.api.routes import router
from app.infrastructure.db import init_db


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
def on_startup():
    init_db()
