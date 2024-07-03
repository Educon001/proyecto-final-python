from . import ingredients, dishes, orders, menu, auth_routes, other_routes
from fastapi import APIRouter

router = APIRouter()
router.include_router(ingredients.router)
router.include_router(dishes.router)
router.include_router(orders.router)
router.include_router(menu.router)
router.include_router(auth_routes.router)
router.include_router(other_routes.router)

del ingredients, dishes, orders, menu
