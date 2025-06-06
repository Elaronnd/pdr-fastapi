from __future__ import annotations
from typing import Optional
from pydantic import (
    BaseModel,
    Field
)


class TestResponse(BaseModel):
    id: int = Field(..., title="Id", description="Id of test")
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the test")
    description: Optional[str] = Field(..., title="Description", min_length=1, max_length=500, description="Description of the test")
    questions: list[QuestionResponse] = Field(
        default_factory=list,
        title="Questions",
        description="List of questions"
    )
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")


from app.schemas.pydantic_questions import QuestionResponse

TestResponse.model_rebuild()