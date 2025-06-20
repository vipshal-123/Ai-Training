from backend.models.User import User
from fastapi.responses import JSONResponse
from beanie import PydanticObjectId
from fastapi.encoders import jsonable_encoder

async def user_date(user: dict):
    print("user", user)
    userId = user.get("_id")
    print("user", userId)
    
    find_user = await User.find_one({ "_id": PydanticObjectId(userId) })
    
    if not find_user:
        return JSONResponse({"success": False, "message":"User not found"}, status_code=404)
    
    return JSONResponse({"success": True, "data": jsonable_encoder(find_user) })