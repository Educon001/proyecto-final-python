from fastapi import FastAPI
from app.routes import router as main_router
from app.infrastructure.db import init_db, Base, engine
from app.auth.routes import router as auth_router

# Inicializa la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluye las rutas de autenticación con el prefijo /auth
app.include_router(auth_router, prefix="/auth")

# Incluye otras rutas
app.include_router(main_router)

# Inicializa la base de datos
@app.on_event("startup")
def on_startup():
    init_db()



# @app.on_event("startup")
# def on_startup():
#     init_db()
