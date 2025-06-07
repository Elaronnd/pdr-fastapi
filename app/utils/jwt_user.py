from jwt.exceptions import InvalidTokenError
from typing import Union
from app.db.queries.users import get_user_by_username
from app.schemas.pydantic_users import UserData
from jwt.api_jwt import (
    decode,
    encode
)
from datetime import (
    datetime,
    timedelta,
    timezone
)
from fastapi import (
    HTTPException,
    status,
    Security
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from app.config.config import (
    JWT_PRIVATE_KEY,
    JWT_PUBLIC_KEY,
    STATUS_CODE
)

security = HTTPBearer()


async def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, JWT_PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt


async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)) -> UserData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode(token.credentials, JWT_PUBLIC_KEY, algorithms="RS256")
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    try:
        user = get_user_by_username(username=username, xss_secure=False)
    except ValueError as error:
        raise HTTPException(status_code=STATUS_CODE.get(str(error).lower()), detail=str(error))
    return UserData(
        id=user.get("id"),
        username=user.get("username"),
        email=user.get("email"),
        password=user.get("password"),
        questions=user.get("questions", []),
        tests=user.get("questions", [])
    )
