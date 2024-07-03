from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import List

from app.infrastructure.db import get_session
from app.infrastructure.repositories import DishRepository
from app.domain.models import Dish, DishCreate, DishPublic, DishItem, DishUpdate

router = APIRouter(prefix="/dishes", tags=["dishes"])


def get_dish_repository(session: Session = Depends(get_session)):
    return DishRepository(session)


@router.get("/", response_model=List[DishPublic], status_code=status.HTTP_200_OK)
def get_dishes(dish_repository: DishRepository = Depends(get_dish_repository)):
    return dish_repository.get_all()


@router.post("/", response_model=DishPublic, status_code=status.HTTP_201_CREATED)
def add_dish(dish: DishCreate, dish_repository: DishRepository = Depends(get_dish_repository)):
    new_dish = Dish(name=dish.name, recipe=dish.recipe, price=dish.price,
                    ingredients=[
                        DishItem(ingredient_id=dish_item.ingredient_id, quantity=dish_item.quantity)
                        for dish_item in dish.ingredients])
    return dish_repository.add(new_dish)


@router.get("/{dish_id}", response_model=DishPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Dish not found"}})
def get_dish(dish_id: UUID, dish_repository: DishRepository = Depends(get_dish_repository)):
    dish = dish_repository.get_by_id(dish_id)
    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT,
               responses={404: {"description": "Dish not found"}})
def delete_dish(dish_id: UUID, dish_repository: DishRepository = Depends(get_dish_repository)):
    deleted = dish_repository.delete(dish_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Dish not found")
    return


@router.put("/{dish_id}", response_model=DishPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Dish not found"}})
def update_dish(dish_id: UUID, dish: DishUpdate, dish_repository: DishRepository = Depends(get_dish_repository)):
    updated = dish_repository.update(dish_id, dish)
    if not updated:
        raise HTTPException(status_code=404, detail="Dish not found")
    return updated
