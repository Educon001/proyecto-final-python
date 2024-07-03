from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.domain.models import User
from app.infrastructure.db import get_session
from app.auth.dependencies import get_current_user  # Importa la dependencia

router = APIRouter(tags=["other"])


@router.get("/protected-route")
def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are authenticated!"}


@router.post("/another-protected-route")
def another_protected_route(data: dict, current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you posted: {data}"}
