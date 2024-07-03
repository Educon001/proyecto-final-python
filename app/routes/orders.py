from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from uuid import UUID
from typing import List

from app.infrastructure.db import get_session
from app.infrastructure.repositories.order_repository import OrderRepository
from app.domain.models import Order, OrderCreate, OrderPublic, OrderItem
from app.domain.enums import OrderStatus

router = APIRouter(prefix="/orders", tags=["orders"])


def get_order_repository(session: Session = Depends(get_session)):
    return OrderRepository(session)


@router.get("/", response_model=List[OrderPublic], status_code=status.HTTP_200_OK)
def get_orders(order_repository: OrderRepository = Depends(get_order_repository)):
    return order_repository.get_all()


@router.post("/", response_model=OrderPublic, status_code=status.HTTP_201_CREATED)
def add_order(order: OrderCreate, order_repository: OrderRepository = Depends(get_order_repository)):
    new_order = Order(
        customer_id=order.customer_id,
        status=order.status,
        items=[
            OrderItem(dish_id=order_item.dish_id, quantity=order_item.quantity)
            for order_item in order.items
        ]
    )
    return order_repository.add(new_order)


@router.get("/{order_id}", response_model=OrderPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Order not found"}})
def get_order(order_id: UUID, order_repository: OrderRepository = Depends(get_order_repository)):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT,
                responses={404: {"description": "Order not found"}})
def delete_order(order_id: UUID, order_repository: OrderRepository = Depends(get_order_repository)):
    deleted = order_repository.delete(order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return


@router.put("/{order_id}", response_model=OrderPublic, status_code=status.HTTP_200_OK,
            responses={404: {"description": "Order not found"}, 400: {"description": "Order already completed"}})
def update_order_status(order_id: UUID, order_repository: OrderRepository = Depends(get_order_repository)):
    order = order_repository.get_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == OrderStatus.Finalizado:
        raise HTTPException(status_code=400, detail="Order already completed")
    order.status = OrderStatus.Finalizado
    order_repository.add(order)
    return order
