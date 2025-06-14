from aiocache import cached
from jwt.exceptions import InvalidTokenError
from typing import Union, Optional

from app.db.queries.users import get_user_by_id
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
    Security,
    Header
)
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer
)
from app.config.config import (
    JWT_PRIVATE_KEY,
    JWT_PUBLIC_KEY
)

security = HTTPBearer(auto_error=False)


async def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update(
        {"exp": expire}
    )
    encoded_jwt = encode(to_encode, JWT_PRIVATE_KEY, algorithm="RS256")
    return encoded_jwt


@cached(ttl=60, key="jwt:{token}")
async def get_current_user(token: HTTPAuthorizationCredentials = Security(security)) -> Optional[UserData]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        return None
    try:
        payload = decode(token.credentials, JWT_PUBLIC_KEY, algorithms="RS256")
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_id(user_id=int(user_id))

    return UserData(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        password=user["password"],
        questions=user["questions"],
        tests=user["questions"],
        is_admin=user["is_admin"]
    )

@cached(ttl=60, key="jwt:{token}")
async def get_current_user_ws(
    token: str = Header(title="JWT token", description="Your JWT token without \"Bearer\"")
) -> Optional[UserData]:
    credentials_exception = HTTPException(
        status_code=403,
        detail="Could not validate credentials"
    )
    try:
        payload = decode(token, JWT_PUBLIC_KEY, algorithms="RS256")
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = await get_user_by_id(user_id=int(user_id))

    return UserData(
        id=user["id"],
        username=user["username"],
        email=user["email"],
        password=user["password"],
        questions=user["questions"],
        tests=user["questions"],
        is_admin=user["is_admin"]
    )
