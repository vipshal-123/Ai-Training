from fastapi import APIRouter

from backend.routes.v1.index import router as v1_router
from backend.routes.auth.index import router as auth_router

router = APIRouter()

router.include_router(prefix="/v1", router=v1_router)
router.include_router(prefix="/auth", router=auth_router)
