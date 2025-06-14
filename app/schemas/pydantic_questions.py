from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    conlist
)
from app.db.check_status import CheckStatus
from app.schemas.pydantic_answers import AnswerCreate, AnswerInQuestionResponse, FullAnswerInQuestionResponse


class QuestionCreate(BaseModel):
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the question")
    description: Optional[str] = Field(title="Description", min_length=1, max_length=500,
                                       description="Description of the test")
    answers: conlist(AnswerCreate, min_length=2, max_length=4) = Field(...,
                                                                       title="Answers",
                                                                       description="List of answers",
                                                                       examples=[
                                                                           [
                                                                               {
                                                                                   "title": "question1",
                                                                                   "is_right": False
                                                                               },
                                                                               {
                                                                                   "title": "question2",
                                                                                   "is_right": True
                                                                               }
                                                                           ]
                                                                       ]
                                                                       )


class QuestionResponse(BaseModel):
    id: int = Field(..., title="Id", description="Id of question")
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the question")
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")

    answers: list[AnswerInQuestionResponse] = Field(
        ...,
        title="Answers",
        description="Answers that contain this question",
    )

    tests_count: Optional[int] = Field(
        default=None,
        title="Tests",
        description="Count of tests that contain this question"
    )


class FullQuestionResponse(QuestionResponse):
    status: CheckStatus = Field(..., title="Status", description="status of question")

    answers: list[FullAnswerInQuestionResponse] = Field(
        ...,
        title="Answers",
        description="Answers that contain this question",
    )

    image_url: Optional[str] = Field(default=None, title="Image url", description="Url to question image")
