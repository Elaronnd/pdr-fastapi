from typing import Optional
from pydantic import (
    BaseModel,
    Field,
    conlist
)


class AnswerCreate(BaseModel):
    title: str = Field(..., title="Title", description="Your answer title", min_length=1, max_length=100)
    is_right: bool = Field(..., title="Is right?", description="Only 1 answer can be right")


class QuestionCreate(BaseModel):
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the question")
    description: Optional[str] = Field(..., title="Description", min_length=1, max_length=500,
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


class AnswerResponse(AnswerCreate):
    id: int = Field(..., title="Id", description="Id of answer")
    question_id: int = Field(..., title="Question ID", description="ID of the question this answer belongs to")


class QuestionResponse(BaseModel):
    id: int = Field(..., title="Id", description="Id of question")
    title: str = Field(..., title="Title", min_length=1, max_length=100, description="Title of the question")
    user_id: int = Field(..., title="User ID", description="ID of the user who created the question")

    answers_count: int = Field(
        ...,
        title="Answers",
        description="Count of answers that contain this question",
    )

    tests_count: Optional[int] = Field(
        default=None,
        title="Tests",
        description="Count of tests that contain this question"
    )
