from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import List

from app.infrastructure.db import get_session
from app.infrastructure.repositories.ingredient_repository import IngredientRepository
from app.domain.models import Ingredient, IngredientCreate, IngredientPublic, IngredientUpdate

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


def get_ingredient_repository(session: Session = Depends(get_session)):
    return IngredientRepository(session)


@router.get("/", response_model=List[IngredientPublic], status_code=status.HTTP_200_OK)
def get_ingredientes(ingredient_repository: IngredientRepository = Depends(get_ingredient_repository)):
    return ingredient_repository.get_all()


@router.post("/", response_model=IngredientPublic, status_code=status.HTTP_201_CREATED)
def add_ingredient(ingredient: IngredientCreate, Ingredient_repository: IngredientRepository = Depends(get_ingredient_repository)):
    new_ingredient = Ingredient(name=ingredient.name, quantity=ingredient.quantity, storage=ingredient.storage)
    return Ingredient_repository.add(new_ingredient)


@router.get("/{ingredient_id}", response_model=IngredientPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Ingredient not found"}})
def get_ingredient(ingredient_id: UUID, ingredient_repository: IngredientRepository = Depends(get_ingredient_repository)):
    ingredient = ingredient_repository.get_by_id(ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT,
               responses={404: {"description": "Ingredient not found"}})
def delete_ingredient(ingredient_id: UUID, ingredient_repository: IngredientRepository = Depends(get_ingredient_repository)):
    deleted = ingredient_repository.delete(ingredient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return


@router.put("/{ingredient_id}", response_model=Ingredient, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Ingredient not found"}})
def update_ingredient(ingredient_id: UUID, ingredientUpdate: IngredientUpdate, ingredient_repository: IngredientRepository = Depends(get_ingredient_repository)):
    updated = ingredient_repository.update(ingredient_id, ingredientUpdate)
    if not updated:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return updated
