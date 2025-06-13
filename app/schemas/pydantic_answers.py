from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    conlist
)

class AnswerCreate(BaseModel):
    title: str = Field(..., title="Title", description="Your answer title", min_length=1, max_length=100)
    is_right: bool = Field(..., title="Is right?", description="Only 1 answer can be right")


class AnswerInQuestionResponse(AnswerCreate):
    id: int = Field(..., title="Id", description="Id of answer")

class FullAnswerInQuestionResponse(AnswerInQuestionResponse):
    image_url: Optional[str] = Field(default=None, title="Image url", description="Url to answer image")

class AnswerResponse(AnswerInQuestionResponse):
    question_id: int = Field(..., title="Question ID", description="ID of the question this answer belongs to")
