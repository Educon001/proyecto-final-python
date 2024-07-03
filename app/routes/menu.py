from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from uuid import UUID
from typing import List

from app.infrastructure.db import get_session
from app.infrastructure.repositories.dish_repository import DishRepository
from app.domain.models import Menu, MenuCreate, MenuPublic


router = APIRouter(prefix="/menus", tags=["menus"])


@router.get("/", response_model=List[MenuPublic], status_code=status.HTTP_200_OK)
def get_menus(session: Session = Depends(get_session)):
    statement = select(Menu)
    result = session.exec(statement).all()
    return list(result)


@router.post("/", response_model=MenuPublic, status_code=status.HTTP_201_CREATED)
def add_menu(menu: MenuCreate, session: Session = Depends(get_session)):
    dish_repository = DishRepository(session)
    dishes = [dish_repository.get_by_id(dish_id) for dish_id in menu.dishes]
    new_menu = Menu(dishes=dishes)
    session.add(new_menu)
    session.commit()
    session.refresh(new_menu)
    return new_menu


@router.get("/{menu_id}", response_model=MenuPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Menu not found"}})
def get_menu(menu_id: UUID, session: Session = Depends(get_session)):
    result = session.get(Menu, menu_id)
    if not result:
        raise HTTPException(status_code=404, detail="Menu not found")
    return result


@router.delete("/{menu_id}", status_code=status.HTTP_204_NO_CONTENT,
                responses={404: {"description": "Menu not found"}})
def delete_menu(menu_id: UUID, session: Session = Depends(get_session)):
    result = session.get(Menu, menu_id)
    if not result:
        raise HTTPException(status_code=404, detail="Menu not found")
    session.delete(result)
    session.commit()
    return


@router.put("/{menu_id}/add_dishes", response_model=MenuPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Menu not found"}})
def add_menu_dishes(menu_id: UUID, menu: MenuCreate, session: Session = Depends(get_session)):
    result = session.get(Menu, menu_id)
    if not result:
        raise HTTPException(status_code=404, detail="Menu not found")
    dish_repository = DishRepository(session)
    dishes = [dish_repository.get_by_id(dish_id) for dish_id in menu.dishes]
    result.dishes.extend(dishes)
    session.commit()
    session.refresh(result)
    return result


@router.put("/{menu_id}/remove_dishes", response_model=MenuPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Menu not found"}})
def remove_menu_dishes(menu_id: UUID, menu: MenuCreate, session: Session = Depends(get_session)):
    result = session.get(Menu, menu_id)
    if not result:
        raise HTTPException(status_code=404, detail="Menu not found")
    dish_repository = DishRepository(session)
    dishes = [dish_repository.get_by_id(dish_id) for dish_id in menu.dishes]
    try:
        for dish in dishes:
            result.dishes.remove(dish)
        session.commit()
        session.refresh(result)
    except Exception:
        raise HTTPException(status_code=404, detail="Dish not found")
    return result

