from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID, uuid4
from app.domain.enums import OrderStatus, UserRole, StorageType


# Entity
class Ingredient(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    quantity: float
    storage: StorageType


# Entity
class DishItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    ingredient_id: UUID = Field(foreign_key="ingredient.id")
    ingredient: Ingredient = Relationship()
    quantity: float
    dish_id: UUID = Field(foreign_key="dish.id")


# Aggregate
class Dish(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    ingredients: List[DishItem] = Relationship()
    recipe: str
    price: float
    menu_id: UUID = Field(foreign_key="menu.id")


# Aggregate
class Menu(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    dishes: List[Dish] = Relationship()


# Entity
class OrderItem(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    dish_id: UUID = Field(foreign_key="dish.id")
    dish: Dish = Relationship()
    quantity: int
    order_id: UUID = Field(foreign_key="order.id")


# Entity
class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str
    password: str
    role: UserRole


# Entity
class Customer(User):
    role: UserRole = UserRole.Customer


# Aggregate
class Order(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    items: List[OrderItem] = Relationship()
    total: float
    status: OrderStatus
    customer_id: UUID = Field(foreign_key="user.id")
    customer: User = Relationship()

