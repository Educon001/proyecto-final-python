from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID
from typing import List
from pydantic import BaseModel

from app.infrastructure.db import get_session
from app.infrastructure.repositories import DishRepository
from app.domain.models import Dish, DishItem

router = APIRouter(prefix="/dishes", tags=["dishes"])


class DishItemCreate(BaseModel):
    ingredient_id: UUID
    quantity: float


class DishCreate(BaseModel):
    name: str
    recipe: str
    price: float
    ingredients: List[DishItemCreate]


class DishResponse(BaseModel):
    name: str
    recipe: str
    price: float
    ingredients: List[DishItem]


def get_dish_repository(session: Session = Depends(get_session)):
    return DishRepository(session)


@router.get("/")
def get_dishes(dish_repository: DishRepository = Depends(get_dish_repository)):
    return dish_repository.get_all()


@router.post("/")
def add_dish(dish: DishCreate, dish_repository: DishRepository = Depends(get_dish_repository)):
    new_dish = Dish(name=dish.name, recipe=dish.recipe, price=dish.price, ingredients=dish.ingredients)
    return dish_repository.add(new_dish)


@router.get("/{dish_id}", response_model=DishResponse)
def get_dish(dish_id: UUID, dish_repository: DishRepository = Depends(get_dish_repository)):
    dish = dish_repository.get_by_id(dish_id)
    response = DishResponse(name=dish.name, recipe=dish.recipe, price=dish.price, ingredients=dish.ingredients)
    return response


@router.delete("/{dish_id}")
def delete_dish(dish_id: UUID, dish_repository: DishRepository = Depends(get_dish_repository)):
    return dish_repository.delete(dish_id)
