from fastapi import APIRouter, HTTPException, Depends
from app.db.check_status import CheckStatus
from app.schemas.pydantic_questions import (
    FullQuestionResponse
)
from app.db.queries import (
    edit_status_question
)
from app.schemas.pydantic_users import UserData
from app.utils.jwt_user import get_current_user

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.post("/{question_id}", response_model=FullQuestionResponse)
async def change_status_question(
    question_id: int,
    status: CheckStatus,
    xss_secure: bool = True,
    current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")
    question = edit_status_question(
        question_id=question_id,
        status=status,
        xss_secure=xss_secure
    )
    return FullQuestionResponse(
        id=question["id"],
        title=question["title"],
        user_id=question["user_id"],
        answers=question["answers"],
        status=question["status"]
    )
