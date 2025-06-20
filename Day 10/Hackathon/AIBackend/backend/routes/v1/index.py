from fastapi import APIRouter

from backend.routes.v1.user import router as user_router

router = APIRouter()

router.include_router(prefix="/user", router=user_router)