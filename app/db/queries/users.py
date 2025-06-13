from app.db.base import Session
from app.db.models import Users
from app.schemas.pydantic_users import email_str_validator
from app.exceptions.users import UserIdError, UsernameError


def get_user_by_id(user_id: int, xss_secure: bool = True):
    with Session() as session:
        user = session.query(Users).filter_by(id = user_id).one_or_none()

        if user is None:
            raise UserIdError(message="User not found", status_code=404, user_id=user_id)
        
        return user.to_dict(xss_secure=xss_secure)


def is_email_in_db(email: email_str_validator) -> bool:
    with Session() as session:
        email = session.query(Users).filter_by(email=email).one_or_none()
        if email is None:
            return False
        return True


def register_user(username: str, password: str, email: email_str_validator, is_admin: bool = False) -> None:
    with Session() as session:
        user = session.query(Users).filter_by(username=username.lower()).one_or_none()

        if user is not None:
            raise UsernameError(message="User already exists", status_code=409, username=username)
        elif is_email_in_db(email=email) is True:
            raise UserIdError(message="This email already registered", status_code=409, user_id=user.id)

        user = Users(username=username.lower(), password=password, email=email, is_admin=is_admin)
        session.add(user)
        session.commit()


def get_user_by_username(username: str, xss_secure: bool = True) -> Users.to_dict:
    with Session() as session:
        user = session.query(Users).filter_by(username=username.lower()).one_or_none()

        if not user:
            raise UsernameError(message="User not found", status_code=404, username=username)

        return user.to_dict(xss_secure=xss_secure)
