from typing import Optional
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


def create_test_db(title: str, user_id: int, questions_id: list[int], description: Optional[str] = None,
                   xss_secure: bool = True):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).one_or_none()

        if not user:
            raise UserIdError(message="User not found", user_id=user_id, status_code=404)

        test = Tests(title=title, description=description, user_id=user_id)
        session.add(test)
        session.flush()

        questions_ids = [question_id for question_id in questions_id]

        questions = session.query(Questions).filter(Questions.id.in_(questions_ids)).all()

        found_ids = {question.id for question in questions}

        unfounded_questions = set(questions_ids) - found_ids

        if unfounded_questions:
            raise QuestionsListError(message="Question(s) not found", questions_id=list(unfounded_questions), status_code=404)

        for question in questions:
            if question.status != CheckStatus.APPROVED:
                raise QuestionError(message="The question is still pending or has been dismissed", status_code=403, question_id=question.id)

            questions_to_tests_obj = QuestionsToTests(
                test_id=test.id,
                question_id=question.id
            )
            session.add(questions_to_tests_obj)

        session.commit()
        session.refresh(test)

        return test.to_dict(xss_secure=xss_secure)


def delete_test(test_id: int):
    with Session() as session:
        test = session.query(Tests).filter_by(id=test_id).one_or_none()

        if not test:
            raise TestError(message="test not found", status_code=404, test_id=test_id)

        session.delete(test)
        session.commit()


def get_all_tests(xss_secure: bool = True):
    with Session() as session:
        tests = session.query(Tests).all()

        if not tests:
            raise TestsError(message="tests not found", status_code=404)

        return [test.to_dict(xss_secure=xss_secure) for test in tests]


def get_test_by_id(test_id: int, xss_secure: bool = True):
    with Session() as session:
        test = session.query(Tests).filter_by(id=test_id).one_or_none()

        if not test:
            raise TestError(message="test not found", status_code=404, test_id=test_id)

        return test.to_dict(xss_secure=xss_secure)
