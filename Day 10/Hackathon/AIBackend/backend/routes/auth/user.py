from fastapi import APIRouter, Request , Depends
from backend.validations.v1 import user as user_validation 

from backend.controller.auth import user

router = APIRouter()


@router.post("/google-signin")
async def signin_wrapper(signin_data: user_validation.SignupFormValue, request: Request):
    return await user.signin(signin_data)