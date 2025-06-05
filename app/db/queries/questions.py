from typing import Optional

from app.db.base import (
    Session
)

from app.db.models import (
    Questions,
    Users,
    Answers
)


def create_question_with_answers(title: str, user_id: int, answers: list, description: Optional[str] = None):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).one_or_none()

        if not user:
            raise ValueError(f"User not found")

        question = Questions(title=title, description=description, user_id=user_id)
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

        return question.to_dict()


def delete_question(question_id: int):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise ValueError(f"question not found")

        session.delete(question)
        session.commit()


def get_all_questions():
    with Session() as session:
        questions = session.query(Questions).all()

        if not questions:
            raise ValueError("questions not found")

        return [question.to_dict() for question in questions]


def get_question_by_id(question_id: int):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise ValueError("question not found")

        return question.to_dict()
