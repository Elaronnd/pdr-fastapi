from typing import Annotated
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    BeforeValidator
)


def strip_and_lower(v: object) -> str:
    return str(v).strip().lower()


email_str_validator = Annotated[
    EmailStr,
    BeforeValidator(strip_and_lower)
]


class Login(BaseModel):
    username: str = Field(..., min_length=1, max_length=100, title="Username", description="Your username")
    password: str = Field(..., title="Password",
                          description="Must be restricted to, though does not specifically require any of:"
                                      "\nuppercase letters: A-Z"
                                      "\nlowercase letters: a-z"
                                      "\nnumbers: 0-9"
                                      "\nany of the special characters: @#$%^&+="
                                      "\nfrom 5 to 35 characters",
                          pattern=r"[A-Za-z0-9@#$%^&+=]{5,35}")


class Register(Login):
    email: email_str_validator = Field(..., title="Email", description="Your email address")


class Token(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    username: str = Field(..., min_length=1, max_length=100, title="Username", description="Your username")
    email: email_str_validator = Field(..., title="Email", description="Your email address")
    questions: list = Field(..., title="Questions", description="List of questions")
    tests: list = Field(..., title="Tests", description="List of Tests")


class FullUserResponse(UserResponse):
    is_admin: bool = Field(..., title="Is admin?", description="Is admin this user?")


class UserData(UserResponse):
    id: int = Field(..., title="Id", description="Id of user")
    password: str = Field(..., title="Password", description="Your password in hash")
    is_admin: bool = Field(..., title="Is admin?", description="Is admin in bool")
