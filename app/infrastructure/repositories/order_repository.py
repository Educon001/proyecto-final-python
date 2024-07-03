from typing import Optional, List
from sqlmodel import Session, select
from fastapi import Depends
from app.infrastructure.db import get_session
from app.domain.repositories import IRepository
from uuid import UUID
from app.domain.models import Order


class OrderRepository(IRepository[Order]):
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(self) -> Optional[List[Order]]:
        statement = select(Order)
        result = self.session.exec(statement).all()
        return list(result)

    def add(self, order: Order) -> Order:
        self.session.add(order)
        self.session.commit()
        self.session.refresh(order)
        order.total = sum([order_item.dish.price * order_item.quantity for order_item in order.items])
        self.session.commit()
        self.session.refresh(order)
        return order

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        result = self.session.get(Order, order_id)
        return result

    def delete(self, order_id: UUID) -> Optional[UUID]:
        result = self.session.get(Order, order_id)
        if result:
            self.session.delete(result)
            self.session.commit()
            return order_id
        return None
