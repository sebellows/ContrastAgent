from fastapi import APIRouter

from .products import pro

router = APIRouter(prefix="/v1")
router.include_router(login_router)
