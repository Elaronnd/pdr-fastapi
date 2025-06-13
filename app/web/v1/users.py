from datetime import timedelta
from app.db.queries import get_user_by_id
from passlib.context import CryptContext
from app.exceptions import UserIdError, UsernameError
from fastapi import (
    APIRouter,
    Depends
)
from app.db.queries.users import (
    register_user,
    get_user_by_username
)
from app.jwt.users import (
    create_access_token,
    get_current_user
)
from app.config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.pydantic_users import (
    Register,
    Token,
    Login,
    UserResponse,
    FullUserResponse,
    UserData
)
from html import escape

users_router = APIRouter(prefix="/users", tags=["Users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.get("/profile/{user_id}", response_model=FullUserResponse)
async def get_user_profile(
    user_id: int,
    xss_secure: bool = True
):
    user = await get_user_by_id(user_id, xss_secure=xss_secure)

    if not user:
        raise UserIdError(status_code=404, message="user not found", user_id=user_id)
    
    return FullUserResponse(
        username=user["username"],
        email=user["email"],
        questions=user["questions"],
        tests=user["tests"],
        is_admin=user["is_admin"]
    )


@users_router.post("/register", response_model=Token)
async def create_user(user: Register):
    password_hash = pwd_context.hash(user.password.lower())
    await register_user(username=user.username.lower(), password=password_hash, email=user.email, is_admin=False)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username.lower()}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@users_router.post("/login", response_model=Token)
async def login(user: Login):
    user_password = await get_user_by_username(username=user.username.lower())
    user_password = user_password.get("password")

    if not pwd_context.verify(user.password.lower(), user_password):
        raise UsernameError(status_code=400, message='Invalid password', username=user.username)

    access_token = await create_access_token(data={"sub": user.username.lower()})
    return Token(access_token=access_token, token_type="bearer")


@users_router.get("/profile", response_model=UserResponse)
async def read_users_me(
    current_user: UserData = Depends(get_current_user),
    xss_secure: bool = True
):
    return UserResponse(
        username=current_user.username if xss_secure is False else escape(current_user.username),
        email=current_user.email if xss_secure is False else escape(current_user.email),
        questions=current_user.questions,
        tests=current_user.tests
    )
