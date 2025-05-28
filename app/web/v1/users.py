from fastapi import APIRouter, HTTPException

from app.db.queries import (
    get_user_by_id
)


users_router = APIRouter(prefix="/users")

@users_router.get("/profile/{user_id}")
async def get_user_profile(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return user