from . import dishes, routes
from fastapi import APIRouter

router = APIRouter()
router.include_router(dishes.router)
router.include_router(routes.router)


del dishes, routes
