from app.db.base import Session
from app.db.models import Users
from app.schemas.users_schema import email_str_validator


def get_user_by_id(user_id: int):
    with Session() as session:
        user = session.query(Users).filter_by(id = user_id).one_or_none()

        if user is None:
            return None
        
        return user.to_dict()


def is_email_in_db(email: email_str_validator) -> bool:
    with Session() as session:
        email = session.query(Users).filter_by(email=email).one_or_none()
        if email is None:
            return False
        return True


def register_user(username: str, password: str, email: email_str_validator) -> None:
    with Session() as session:
        user = session.query(Users).filter_by(username=username.lower()).one_or_none()


        if user is not None:
            raise ValueError("User already exists")
        elif is_email_in_db(email=email) is True:
            raise ValueError("This email already registered")

        user = Users(username=username.lower(), password=password, email=email)
        session.add(user)
        session.commit()


def get_user_by_username(username: str) -> Users.to_dict:
    with Session() as session:
        user = session.query(Users).filter_by(username=username.lower()).one_or_none()

        if not user:
            raise ValueError('User not found')

        return user.to_dict()


def get_password_by_username(username: str) -> Users.password:
    with Session() as session:
        user = session.query(Users).filter_by(username=username.lower()).one_or_none()

        if not user:
            raise ValueError('User not found')

        return user.password
