from fastapi import APIRouter, HTTPException, Depends
from app.services.tests import delete_test_func
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user

admin_tests_router = APIRouter(prefix="/tests")


@admin_tests_router.delete("/{question_id}")
async def delete_question_admin(
        test_id: int,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")

    return await delete_test_func(test_id=test_id, is_admin=True)
