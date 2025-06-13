from fastapi import APIRouter, HTTPException, Depends, Response
from app.db.check_status import CheckStatus
from app.db.queries.users import get_user_by_username
from app.exceptions import QuestionError
from app.schemas.pydantic_questions import (
    QuestionCreate,
    QuestionResponse,
    FullQuestionResponse
)
from app.db.queries import (
    create_question_with_answers,
    delete_question,
    get_all_questions,
    get_question_by_id
)
from app.schemas.pydantic_users import UserData
from app.utils.jwt_user import get_current_user

questions_router = APIRouter(prefix="/questions", tags=["Questions"])


@questions_router.post("/", response_model=QuestionResponse)
async def add_question(
    question: QuestionCreate,
    current_user: UserData = Depends(get_current_user),
    xss_secure: bool = True
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    right_answers = 0
    for answer in question.answers:
        if answer.is_right is True:
            right_answers = right_answers + 1
    if right_answers != 1:
        raise HTTPException(
            status_code=413,
            detail="There must be exactly one correct answer"
        )
    created_question = create_question_with_answers(
        title=question.title,
        description=question.description,
        user_id=current_user.id,
        answers=question.answers,
        xss_secure=xss_secure,
        status=CheckStatus.APPROVED if current_user.is_admin is True else CheckStatus.PENDING
    )
    return QuestionResponse(
        id=created_question["id"],
        title=created_question["title"],
        user_id=created_question["user_id"],
        answers=created_question["answers"],
    )


@questions_router.delete("/{question_id}")
async def delete_question_api(
        question_id: int,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    user_data = get_user_by_username(username=current_user.username)
    user_questions = user_data.get("questions", [])

    if any(question.get("id") == question_id for question in user_questions) or current_user.is_admin is True:
        delete_question(question_id=question_id)
        return Response(status_code=204)

    raise HTTPException(status_code=403, detail="You don't have permission to delete this question")


@questions_router.get("/", response_model=list[QuestionResponse])
async def get_all_questions_api(
        xss_secure: bool = True,
        current_user: UserData = Depends(get_current_user)
):
    questions = get_all_questions(xss_secure=xss_secure, status=None if current_user.is_admin is True else CheckStatus.APPROVED)
    return [
        QuestionResponse(
            id=question["id"],
            title=question["title"],
            user_id=question["user_id"],
            answers=question["answers"],
            tests_count=question["test_count"]
        )
        for question in questions
    ]


@questions_router.get("/{question_id}", response_model=FullQuestionResponse)
async def get_question_by_id_api(question_id: int, xss_secure: bool = True, current_user: UserData = Depends(get_current_user)):
    question = get_question_by_id(question_id=question_id, xss_secure=xss_secure)
    if question.get("status") != CheckStatus.APPROVED and (current_user is None or question.get("user_id") != current_user.id and current_user.is_admin is False):
        raise QuestionError(status_code=423, message="Question awaiting review", question_id=question_id)
    return FullQuestionResponse(
        id=question["id"],
        title=question["title"],
        user_id=question["user_id"],
        answers=question["answers"],
        tests_count=question["test_count"],
        status=question["status"]
    )
