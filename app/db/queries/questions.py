from app.db.base import (
    Session
)

from app.db.models import (
    Questions,
    Users
)

def create_question(title: str, user_id: int):
    with Session() as session:
        user = session.query(Users).filter_by(id=user_id).one_or_none()

        if not user:
            raise ValueError(f"User with id {user_id} does not exist.")
        

        question = Questions(title=title, user_id=user_id)
        session.add(question)
        session.commit()

def delete_question(question_id: int):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise ValueError(f"Question with id {question_id} does not exist.")
        
        session.delete(question)
        session.commit()

def get_all_questions():
    with Session() as session:
        questions = session.query(Questions).all()
        return [question.to_dict() for question in questions]
    
def get_question_by_id(question_id: int):
    with Session() as session:
        question = session.query(Questions).filter_by(id=question_id).one_or_none()

        if not question:
            raise ValueError(f"Question with id {question_id} does not exist.")
        
        return question.to_dict()