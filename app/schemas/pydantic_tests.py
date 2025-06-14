from typing import Optional
from app.schemas.pydantic_questions import QuestionResponse, FullQuestionResponse
from pydantic import (
    BaseModel,
    Field,
    conlist
)

class BaseTest(BaseModel):
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the test")
    description: Optional[str] = Field(title="Description", min_length=1, max_length=500,
                                       description="Description of the test")

class TestCreate(BaseTest):
    questions_id: conlist(int, min_length=2, max_length=20) = Field(..., title="Questions list", description="List of questions ids")


class TestResponse(BaseTest):
    id: int = Field(..., title="Id", description="Id of test")
    questions: list[QuestionResponse] = Field(
        default_factory=list,
        title="Questions",
        description="List of questions"
    )
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")


class FullTestResponse(TestResponse):
    questions: list[FullQuestionResponse] = Field(
        default_factory=list,
        title="Questions",
        description="List of questions"
    )
