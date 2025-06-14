from typing import Optional
from aiocache import cached
from fastapi import Response, HTTPException
from app.cloud.r2_cloudflare import r2_client
from app.db.check_status import CheckStatus
from app.db.queries import get_all_questions, get_question_by_id
from app.db.queries.questions import edit_question, delete_question, create_question_with_answers
from app.exceptions import QuestionError
from app.schemas.pydantic_answers import AnswerInQuestionResponse, FullAnswerInQuestionResponse
from app.schemas.pydantic_questions import QuestionResponse, FullQuestionResponse, QuestionCreate


@cached(ttl=60, key="questions:{is_admin}")
async def get_all_questions_func(
        is_admin: bool,
        xss_secure: bool = True
):
    questions = await get_all_questions(xss_secure=xss_secure, status=CheckStatus.APPROVED if is_admin is False else None)
    return [
        QuestionResponse(
            id=question["id"],
            title=question["title"],
            user_id=question["user_id"],
            answers=[
                AnswerInQuestionResponse(
                    id=answer["id"],
                    title=answer["title"],
                    is_right=answer["is_right"]
                ) for answer in question["answers"]
            ],
            tests_count=question["test_count"]
        )
        for question in questions
    ]


async def get_question_func(
    question_id: int,
    is_admin: bool,
    user_id: Optional[int] = None,
    xss_secure: bool = True
):
    question = await get_question_by_id(question_id=question_id, xss_secure=xss_secure)
    if question.get("status") != CheckStatus.APPROVED and (user_id is None or question["user_id"] != user_id and is_admin is False):
        raise QuestionError(status_code=423, message="Question awaiting review", question_id=question_id)
    return FullQuestionResponse(
        id=question["id"],
        title=question["title"],
        user_id=question["user_id"],
        answers=[
            FullAnswerInQuestionResponse(
                id=answer["id"],
                title=answer["title"],
                is_right=answer["is_right"],
                image_url=None if answer["filename"] is None else r2_client.generate_image_url(
                    filename=f"answers/{answer['filename']}")
            ) for answer in question["answers"]
        ],
        tests_count=question["test_count"],
        status=question["status"],
        image_url=None if question["filename"] is None else r2_client.generate_image_url(
            filename=f"questions/{question['filename']}")
    )


async def edit_question_func(
        question_id: int,
        is_admin: bool,
        title: str = None,
        description: str = None,
        xss_secure: bool = True
):
    question = await edit_question(question_id=question_id, title=title, description=description, xss_secure=xss_secure, status=CheckStatus.PENDING if is_admin is False else CheckStatus.APPROVED)

    return FullQuestionResponse(
        id=question["id"],
        title=question["title"],
        user_id=question["user_id"],
        answers=[
            FullAnswerInQuestionResponse(
                id=answer["id"],
                title=answer["title"],
                is_right=answer["is_right"],
                image_url=None if answer["filename"] is None else r2_client.generate_image_url(filename=f"answers/{answer['filename']}")
            ) for answer in question["answers"]
        ],
        tests_count=question["test_count"],
        status=question["status"],
        image_url=None if question["filename"] is None else r2_client.generate_image_url(filename=f"questions/{question['filename']}")
    )


async def delete_question_func(
        question_id: int,
        is_admin: bool,
        user_id: Optional[int] = None
):
    question_info = await get_question_by_id(question_id=question_id)

    if question_info["id"] == user_id or is_admin is True:
        await delete_question(question_id=question_id)
        return Response(status_code=204)

    raise HTTPException(status_code=403, detail="You don't have permission to delete this question")


async def add_question_func(
    question: QuestionCreate,
    is_admin: bool,
    user_id: int,
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
    created_question = await create_question_with_answers(
        title=question.title,
        description=question.description,
        user_id=user_id,
        answers=question.answers,
        xss_secure=xss_secure,
        status=CheckStatus.APPROVED if is_admin is True else CheckStatus.PENDING
    )
    return QuestionResponse(
        id=created_question["id"],
        title=created_question["title"],
        user_id=created_question["user_id"],
        answers=[
            AnswerInQuestionResponse(
                id=answer["id"],
                title=answer["title"],
                is_right=answer["is_right"]
            ) for answer in created_question["answers"]
        ],
    )
