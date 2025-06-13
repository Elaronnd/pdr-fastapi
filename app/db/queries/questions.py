from typing import Optional
from app.db.base import Session
from app.db.check_status import CheckStatus
from app.exceptions import QuestionsError, QuestionError, UserIdError
from app.db.models import (
    Questions,
    Users,
    Answers
)


def create_question_with_answers(title: str, user_id: int, answers: list, status: CheckStatus, description: Optional[str] = None, xss_secure: bool = True):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).one_or_none()

        if not user:
            raise UserIdError(message="User not found", user_id=user_id, status_code=404)

        question = Questions(title=title, description=description, user_id=user_id, status=status)
        session.add(question)
        session.flush()

        for answer in answers:
            answer_obj = Answers(
                title=answer.title,
                is_right=answer.is_right,
                question_id=question.id
            )
            session.add(answer_obj)

        session.commit()
        session.refresh(question)

        return question.to_dict(xss_secure=xss_secure)


def delete_question(question_id: int):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        session.delete(question)
        session.commit()


def edit_status_question(question_id: int, status: CheckStatus, xss_secure: bool = True):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        question.status = status

        session.commit()
        session.refresh(question)

        return question.to_dict(xss_secure=xss_secure)


def get_all_questions(status: Optional[CheckStatus] = None, xss_secure: bool = True):
    with Session() as session:
        if status is None:
            questions = session.query(Questions).all()
        else:
            questions = session.query(Questions).filter_by(status=status).all()

        if not questions:
            raise QuestionsError(message="questions not found", status_code=404)

        return [question.to_dict(xss_secure=xss_secure) for question in questions]


def get_question_by_id(question_id: int, xss_secure: bool = True):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise QuestionError(message="question not found", status_code=404, question_id=question_id)

        return question.to_dict(xss_secure=xss_secure)
