from . import ingredients, dishes, orders, routes
from fastapi import APIRouter

router = APIRouter()
router.include_router(ingredients.router)
router.include_router(dishes.router)
router.include_router(orders.router)
router.include_router(routes.router)


del ingredients, dishes, orders, routes
