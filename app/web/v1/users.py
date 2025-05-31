from datetime import timedelta
from app.db.queries import get_user_by_id
from passlib.context import CryptContext
from fastapi import (
    APIRouter,
    HTTPException,
    Depends
)
from app.db.queries.users import (
    register_user,
    get_password_by_username
)
from app.utils.jwt_user import (
    create_access_token,
    get_current_user
)
from app.config.config import (
    STATUS_CODE,
    ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.utils.pydantic_classes import (
    Register,
    Token,
    Login,
    UserResponse,
    UserData
)

users_router = APIRouter(prefix="/users")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@users_router.get("/profile/{user_id}", response_model=UserResponse)
async def get_user_profile(user_id: int):
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    
    return UserResponse(
        username=user.get("username"),
        email=user.get("email"),
        questions=user.get("questions"),
        tests=user.get("tests")
    )


@users_router.post("/register", response_model=Token)
async def create_user(user: Register):
    password_hash = pwd_context.hash(user.password.lower())
    try:
        register_user(username=user.username.lower(), password=password_hash, email=user.email)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username.lower()}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@users_router.post("/login", response_model=Token)
async def login(user: Login):
    try:
        user_password = get_password_by_username(username=user.username.lower())
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))

    if not pwd_context.verify(user.password.lower(), user_password):
        raise HTTPException(status_code=400, detail='Invalid password')

    access_token = await create_access_token(data={"sub": user.username.lower()})
    return Token(access_token=access_token, token_type="bearer")


@users_router.get("/profile", response_model=UserResponse)
async def read_users_me(current_user: UserData = Depends(get_current_user)):
    return UserResponse(
        username=current_user.username,
        email=current_user.email,
        questions=current_user.questions,
        tests=current_user.tests
    )
