from typing import Optional, List
from sqlmodel import Session, select
from fastapi import Depends
from app.infrastructure.db import get_session
from app.domain.repositories import IRepository
from uuid import UUID
from app.domain.models import Dish


class DishRepository(IRepository[Dish]):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(self) -> Optional[List[Dish]]:
        statement = select(Dish)
        result = self.session.exec(statement).all()
        return list(result)

    def add(self, dish: Dish) -> Dish:
        self.session.add(dish)
        self.session.commit()
        self.session.refresh(dish)
        return dish

    def get_by_id(self, dish_id: UUID) -> Optional[Dish]:
        result = self.session.get(Dish, dish_id)
        return result

    def delete(self, dish_id: UUID) -> Optional[UUID]:
        result = self.session.get(Dish, dish_id)
        if result:
            self.session.delete(result)
            self.session.commit()
            return dish_id
        return None
