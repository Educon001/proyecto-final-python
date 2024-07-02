from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.infrastructure.db import get_session
from app.domain.models import Ingredient

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}



@router.get("/ingredients", response_model=list[Ingredient])
def get_ingredients(session: Session = Depends(get_session)):
    result = session.execute(select(Ingredient))
    ingredients = result.scalars().all()
    return ingredients


@router.post("/ingredients")
def add_ingredient(ingredient: Ingredient, session: Session = Depends(get_session)):
    session.add(ingredient)
    session.commit()
    session.refresh(ingredient)
    return ingredient