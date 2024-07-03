from . import dishes, routes, orders
from fastapi import APIRouter

router = APIRouter()
router.include_router(dishes.router)
router.include_router(routes.router)
router.include_router(orders.router)

del dishes, routes, orders
