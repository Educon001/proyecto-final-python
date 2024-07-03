from . import ingredients, dishes, orders, menu
from fastapi import APIRouter

router = APIRouter()
router.include_router(ingredients.router)
router.include_router(dishes.router)
router.include_router(orders.router)
router.include_router(menu.router)


del ingredients, dishes, orders, menu
