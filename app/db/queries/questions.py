from aiocache import cached
from sqlalchemy import select
from typing import Optional
from sqlalchemy.orm import selectinload
from app.cache.db.queries import set_cache, delete_cache
from app.db.queries.answers import delete_answer
from app.db.base import Session
from app.db.check_status import CheckStatus
from app.exceptions import QuestionsError, QuestionError, UserIdError
from app.db.models import (
    Questions,
    Users,
    Answers
)


async def create_question_with_answers(title: str, user_id: int, answers: list, status: CheckStatus, description: Optional[str] = None, xss_secure: bool = True):
    async with Session() as session:
        user = await session.execute(select(Users).where(Users.id == user_id))
        user = user.scalar_one_or_none()

        if not user:
            raise UserIdError(message="User not found", user_id=user_id, status_code=404)

        question = Questions(title=title, description=description, user_id=user_id, status=status)
        session.add(question)
        await session.flush()

        for answer in answers:
            answer_obj = Answers(
                title=answer.title,
                is_right=answer.is_right,
                user_id=user_id,
                question_id=question.id
            )
            session.add(answer_obj)

        await session.commit()

        await session.refresh(question)

        question = await session.execute(
            select(Questions)
            .options(
                selectinload(Questions.answers),
                selectinload(Questions.test_questions)
            )
            .where(Questions.id == question.id)
        )
        question = question.scalar_one()

        result = question.to_dict(xss_secure=xss_secure)

        await set_cache(key="question", cache_id=question.id, value=result)
        await set_cache(key="questions", cache_id=True, value=result)

        if status == CheckStatus.APPROVED:
            await set_cache(key="questions", cache_id=False, value=result)

        return result


async def delete_question(
        question_id: int
):
    async with Session() as session:
        question = await session.execute(
            select(Questions)
            .options(selectinload(Questions.answers))
            .where(Questions.id == question_id)
        )
        question = question.scalar_one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        for answer in question.answers:
            await delete_answer(answer_id=answer.id, user_id=answer.user_id)

        await session.delete(question)

        await delete_cache(key="question", cache_id=question_id)
        await delete_cache(key="questions", cache_id=True)
        await delete_cache(key="questions", cache_id=False)

        await session.commit()


async def edit_status_question(question_id: int, status: CheckStatus, xss_secure: bool = True):
    async with Session() as session:
        question = await session.execute(
            select(Questions)
            .options(
                selectinload(Questions.answers),
                selectinload(Questions.test_questions)
            )
            .where(Questions.id == question_id)
        )
        question = question.scalar_one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        question.status = status

        await session.commit()
        await session.refresh(question)

        return question.to_dict(xss_secure=xss_secure)


async def get_all_questions(status: Optional[CheckStatus] = None, xss_secure: bool = True):
    async with Session() as session:
        if status is None:
            request = select(Questions).options(selectinload(Questions.answers), selectinload(Questions.test_questions))
        else:
            request = select(Questions).where(Questions.status == status).options(selectinload(Questions.answers), selectinload(Questions.test_questions))

        questions = await session.execute(request)
        questions = questions.scalars().all()

        if not questions:
            raise QuestionsError(message="questions not found", status_code=404)

        return [question.to_dict(xss_secure=xss_secure) for question in questions]


@cached(ttl=60, key="question:{question_id}")
async def get_question_by_id(question_id: int, xss_secure: bool = True):
    async with Session() as session:
        question = await session.execute(
            select(Questions)
            .options(
                selectinload(Questions.answers),
                selectinload(Questions.test_questions)
            )
            .where(Questions.id == question_id)
        )
        question = question.scalar_one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        return question.to_dict(xss_secure=xss_secure)



async def is_owner_user(
    question_id: int,
    user_id: int
) -> bool:
    async with Session() as session:
        question = await session.execute(select(Questions).where(Questions.id == question_id))
        question = question.scalar_one_or_none()

        if not question:
            raise QuestionError(message="answer not found", status_code=404, question_id=question_id)
        elif question.user_id != user_id:
            return False
        return True


async def edit_question(
        question_id: int,
        status: CheckStatus = None,
        title: str = None,
        description: str = None,
        filename: str = None,
        xss_secure: bool = True
):
    async with Session() as session:
        question = await session.execute(
            select(Questions)
            .where(Questions.id == question_id)
            .options(
                selectinload(Questions.answers),
                selectinload(Questions.test_questions)
            )
        )
        question = question.scalar_one_or_none()

        if not question:
            raise QuestionError(message="answer not found", status_code=404, question_id=question_id)
        elif title is not None:
            question.title = title

        if filename is not None:
            question.filename = filename

        if description is not None:
            question.description = description

        if status is not None:
            question.status = status

        await session.commit()
        await session.refresh(question)

        result = question.to_dict(xss_secure=xss_secure)

        await set_cache(key="question", cache_id=question_id, value=result)
        await set_cache(key="questions", cache_id=True, value=result)

        if question.status == CheckStatus.APPROVED:
            await set_cache(key="questions", cache_id=False, value=result)

        return result
