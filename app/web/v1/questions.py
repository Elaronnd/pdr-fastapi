from fastapi import APIRouter, HTTPException, Depends, Response

from app.config.config import STATUS_CODE
from app.db.queries.users import get_user_by_username
from app.schemas.pydantic_questions import (
    QuestionCreate,
    QuestionResponse
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
    right_answers = 0
    for answer in question.answers:
        if answer.is_right is True:
            right_answers = right_answers + 1
    if right_answers != 1:
        raise HTTPException(
            status_code=413,
            detail="There must be exactly one correct answer"
        )
    try:
        created_question = create_question_with_answers(
            title=question.title,
            description=question.description,
            user_id=current_user.id,
            answers=question.answers,
            xss_secure=xss_secure
        )
        return QuestionResponse(
            id=created_question.get("id"),
            title=created_question.get("title"),
            user_id=created_question.get("user_id"),
            answers_count=created_question.get("answers_count"),
        )
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))


@questions_router.delete("/{question_id}")
async def delete_question_api(
        question_id: int,
        current_user: UserData = Depends(get_current_user)
):
    user_data = get_user_by_username(username=current_user.username)
    user_questions = user_data.get("questions", [])

    for question in user_questions:
        if question.get("id") == question_id:
            delete_question(question_id=question_id)
            return Response(status_code=204)

    raise HTTPException(status_code=403, detail="You don't have permission to delete this question")


@questions_router.get("/", response_model=list[QuestionResponse])
async def get_all_questions_api(xss_secure: bool = True):
    questions_list = []
    try:
        questions = get_all_questions(xss_secure=xss_secure)
        for question in questions:
            questions_list.append(
                QuestionResponse(
                    id=question.get("id"),
                    title=question.get("title"),
                    user_id=question.get("user_id"),
                    answers_count=question.get("answers_count"),
                    tests_count=question.get("test_count")
                )
            )
        return questions_list
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))


@questions_router.get("/{question_id}", response_model=QuestionResponse)
async def get_question_by_id_api(question_id: int, xss_secure: bool = True):
    try:
        question = get_question_by_id(question_id=question_id, xss_secure=xss_secure)
        return QuestionResponse(
            id=question.get("id"),
            title=question.get("title"),
            user_id=question.get("user_id"),
            answers_count=question.get("answers_count"),
            tests_count=question.get("test_count")
        )
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))
