from sqlalchemy import select
from typing import Optional

from sqlalchemy.orm import selectinload

from app.db.base import (
    Session
)
from app.exceptions import UserIdError, TestsError, TestError, QuestionError, QuestionsListError
from app.db.check_status import CheckStatus
from app.db.models import (
    Tests,
    Users,
    QuestionsToTests,
    Questions
)


async def create_test_db(
    title: str,
    user_id: int,
    questions_id: list[int],
    description: Optional[str] = None,
    xss_secure: bool = True
) -> dict:
    async with Session() as session:
        # Check if user exists
        user = await session.execute(select(Users).where(Users.id == user_id))
        user = user.scalar_one_or_none()

        if not user:
            raise UserIdError(message="User not found", user_id=user_id, status_code=404)

        # Create test
        test = Tests(title=title, description=description, user_id=user_id)
        session.add(test)
        await session.flush()
        test_id = test.id  # Store id to avoid accessing test.id later

        # Validate questions
        questions_ids = [question_id for question_id in questions_id]
        questions = await session.execute(
            select(Questions)
            .options(
                selectinload(Questions.answers),
                selectinload(Questions.test_questions)
            )
            .where(Questions.id.in_(questions_ids))
        )
        questions = questions.scalars().all()

        found_ids = {question.id for question in questions}
        unfounded_questions = set(questions_ids) - found_ids

        if unfounded_questions:
            raise QuestionsListError(
                message="Question(s) not found",
                questions_id=list(unfounded_questions),
                status_code=404
            )

        for question in questions:
            if question.status != CheckStatus.APPROVED:
                raise QuestionError(
                    message="The question is still pending or has been dismissed",
                    status_code=403,
                    question_id=question.id
                )

            questions_to_tests_obj = QuestionsToTests(
                test_id=test_id,
                question_id=question.id
            )
            session.add(questions_to_tests_obj)

        await session.commit()

        # Fetch test with relationships
        test = await session.execute(
            select(Tests)
            .options(
                selectinload(Tests.questions).options(
                    selectinload(Questions.answers),
                    selectinload(Questions.test_questions)
                )
            )
            .where(Tests.id == test_id)
        )
        test = test.scalar_one_or_none()

        return test.to_dict(xss_secure=xss_secure)


async def delete_test(test_id: int):
    async with Session() as session:
        test = await session.execute(select(Tests).where(Tests.id == test_id))
        test = test.scalar_one_or_none()

        if not test:
            raise TestError(message="test not found", status_code=404, test_id=test_id)

        await session.delete(test)
        await session.commit()


async def get_all_tests(xss_secure: bool = True):
    async with Session() as session:
        tests = await session.execute(
            select(Tests)
            .options(
                selectinload(Tests.questions).options(
                    selectinload(Questions.answers),
                    selectinload(Questions.test_questions)
                )
            )
        )
        tests = tests.scalars().all()

        if not tests:
            raise TestsError(message="tests not found", status_code=404)

        return [test.to_dict(xss_secure=xss_secure) for test in tests]


async def get_test_by_id(test_id: int, xss_secure: bool = True):
    async with Session() as session:
        test = await session.execute(
            select(Tests)
            .options(
                selectinload(Tests.questions).options(
                    selectinload(Questions.answers),
                    selectinload(Questions.test_questions)
                )
            )
            .where(Tests.id == test_id)
        )
        test = test.scalar_one_or_none()

        if not test:
            raise TestError(message="test not found", status_code=404, test_id=test_id)

        return test.to_dict(xss_secure=xss_secure)
