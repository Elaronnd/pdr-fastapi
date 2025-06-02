from typing import Annotated, Optional
from pydantic import (
    BaseModel,
    Field,
    EmailStr,
    BeforeValidator,
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


class UserData(UserResponse):
    password: str = Field(..., title="Password", description="Your password in hash")

class QuestionCreate(BaseModel):
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the question")
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")

class AnswerResponse(BaseModel):
    id: int
    is_right: bool = Field(..., title="Is Right", description="Indicates if the answer is correct")
    question_id: int = Field(..., title="Question ID", description="ID of the question this answer belongs to")


class TestResponse(BaseModel):
    id: int
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the test")
    description: str = Field(..., title="Description", min_length=1, max_length=500, description="Description of the test")


class QuestionResponse(BaseModel):
    id: int
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the qustion")
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")

    answers: Optional[list[AnswerResponse]] = Field(
        default_factory=list,
        title="Answers",
        description="List of answers to the question"
    )

    tests: Optional[list[TestResponse]] = Field(
        default_factory=list,
        title="Tests",
        description="List of tests that contain this question"
    )