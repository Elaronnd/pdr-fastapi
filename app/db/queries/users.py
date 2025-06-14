from aiocache import cached
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.cache.db.queries import set_cache
from app.db.base import Session
from app.db.models import Users, Questions, Tests
from app.schemas.pydantic_users import email_str_validator
from app.exceptions.users import UserIdError, UsernameError, UserError


@cached(ttl=60, key="user:{user_id}")
async def get_user_by_id(user_id: int, xss_secure: bool = True):
    async with Session() as session:
        user = await session.execute(select(Users).options(selectinload(Users.questions),selectinload(Users.tests)).filter_by(id=user_id))
        user = user.scalar_one_or_none()

        if user is None:
            raise UserIdError(message="User not found", status_code=404, user_id=user_id)
        
        return user.to_dict(xss_secure=xss_secure)


@cached(ttl=60, key="is_email_user:{email}")
async def is_email_in_db(email: email_str_validator) -> bool:
    async with Session() as session:
        email = await session.execute(select(Users).where(Users.email == email))
        email = email.one_or_none()
        if email is None:
            return False
        return True


async def register_user(username: str, password: str, email: email_str_validator, is_admin: bool = False) -> Users.to_dict:
    async with Session() as session:
        user = await session.execute(select(Users).where(Users.username == username.lower()))
        user = user.scalar_one_or_none()

        if user is not None:
            raise UsernameError(message="User already exists", status_code=409, username=username)
        elif await is_email_in_db(email=email) is True:
            raise UserError(message="This email already registered", status_code=409)

        user = Users(username=username.lower(), password=password, email=email, is_admin=is_admin)
        session.add(user)
        await session.commit()

        user = await session.execute(
            select(Users)
            .options(
                selectinload(Users.questions).options(
                    selectinload(Questions.answers),
                    selectinload(Questions.test_questions)
                ),
                selectinload(Users.tests).options(
                    selectinload(Tests.questions).options(
                        selectinload(Questions.answers),
                        selectinload(Questions.test_questions)
                    )
                ),
                selectinload(Users.answers)
            )
            .where(Users.username == username.lower())
        )
        user = user.scalar_one_or_none()

        result = user.to_dict(xss_secure=True)

        await set_cache(key="user", cache_id=user.id, value=result)

        return result


async def get_user_by_username(username: str, xss_secure: bool = True) -> dict:
    async with Session() as session:
        user = await session.execute(
            select(Users)
            .options(
                selectinload(Users.questions).options(
                    selectinload(Questions.answers),
                    selectinload(Questions.test_questions)
                ),
                selectinload(Users.tests).options(
                    selectinload(Tests.questions).options(
                        selectinload(Questions.answers),
                        selectinload(Questions.test_questions)
                    )
                ),
                selectinload(Users.answers)
            )
            .where(Users.username == username.lower())
        )
        user = user.scalar_one_or_none()

        if not user:
            raise UsernameError(message="User not found", status_code=404, username=username)

        return user.to_dict(xss_secure=xss_secure)
