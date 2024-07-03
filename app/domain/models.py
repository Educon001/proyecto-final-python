from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from uuid import UUID, uuid4
from app.domain.enums import OrderStatus, UserRole, StorageType


class IngredientBase(SQLModel):
    name: str
    quantity: float
    storage: StorageType


# Entity
class Ingredient(IngredientBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)


class IngredientCreate(IngredientBase):
    pass


class IngredientPublic(IngredientBase):
    id: UUID


class DishItemBase(SQLModel):
    ingredient_id: UUID = Field(foreign_key="ingredient.id")
    quantity: float


# Entity
class DishItem(DishItemBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    dish_id: Optional[UUID] = Field(foreign_key="dish.id")
    ingredient: Ingredient = Relationship()


class DishItemCreate(DishItemBase):
    pass


class DishItemIngredient(SQLModel):
    name: str


class DishItemPublic(SQLModel):
    ingredient: DishItemIngredient
    quantity: float


class DishBase(SQLModel):
    name: str
    recipe: str
    price: float


# Aggregate
class Dish(DishBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    ingredients: List[DishItem] = Relationship()
    menu_id: Optional[UUID] = Field(foreign_key="menu.id")


class DishCreate(DishBase):
    ingredients: List[DishItemCreate]


class DishUpdate(DishBase):
    pass


class DishPublic(DishBase):
    id: UUID
    ingredients: List[DishItemPublic] = None


# Aggregate
class Menu(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    dishes: List[Dish] = Relationship()


class MenuCreate(SQLModel):
    dishes: List[UUID]


class MenuPublic(SQLModel):
    id: UUID
    dishes: List[DishPublic] = None


class OrderItemBase(SQLModel):
    dish_id: UUID = Field(foreign_key="dish.id")
    quantity: int


# Entity
class OrderItem(OrderItemBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    dish: Dish = Relationship()
    order_id: Optional[UUID] = Field(foreign_key="order.id")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemPublic(SQLModel):
    dish: DishPublic
    quantity: int


class UserBase(SQLModel):
    username: str
    role: UserRole
    is_active: bool


# Entity
class User(UserBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str


class UserCreate(UserBase):
    password: str


class UserPublic(UserBase):
    id: UUID


class CustomerCreate(UserCreate):
    role: UserRole = UserRole.Customer


class OrderBase(SQLModel):
    status: OrderStatus
    customer_id: UUID = Field(foreign_key="user.id")


# Aggregate
class Order(OrderBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    items: List[OrderItem] = Relationship()
    customer: User = Relationship()
    total: Optional[float] = Field(default=0.0)


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderPublic(OrderBase):
    id: UUID
    items: List[OrderItemPublic] = None
    customer: UserPublic = None
    total: float
