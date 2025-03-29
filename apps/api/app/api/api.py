from fastapi import APIRouter

from .v1 import products

router = APIRouter()
router.include_router(
    products.router,
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# api_router.include_router(
#     vendors.router,
#     prefix="/vendors",
#     tags=["vendors"],
#     responses={404: {"description": "Not found"}},
# )
