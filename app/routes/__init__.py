from . import ingredients, dishes, orders
from fastapi import APIRouter

router = APIRouter()
router.include_router(ingredients.router)
router.include_router(dishes.router)
router.include_router(orders.router)


del ingredients, dishes, orders
