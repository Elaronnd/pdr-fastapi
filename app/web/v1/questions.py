from fastapi import APIRouter, HTTPException

from app.utils.pydantic_classes import (
    QuestionCreate
)

from app.db.queries import (
    create_question,
    delete_question,
    get_all_questions,
    get_question_by_id
)


questions_router = APIRouter(prefix="/questions", tags=["Питання ❓"])

@questions_router.post("/create")
async def create_question_api(question: QuestionCreate):

    try:

        create_question(
            title=question.title,
            user_id=question.user_id
        )
        return {"message": "Question created successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while creating the question: {str(e)}"
        )

@questions_router.delete("/{question_id}")
async def delete_question_api(question_id: int):

    try:

        delete_question(question_id=question_id)
        return {"message": "Question deleted successfully"}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the question: {str(e)}"
        )
    
@questions_router.get("/all")
async def get_all_questions_api():
    try:

        questions = get_all_questions()
        return {"questions": questions}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching all questions: {str(e)}"
        )
    
@questions_router.get("/{question_id}")
async def get_question_by_id_api(question_id: int):
    try:

        question = get_question_by_id(question_id=question_id)
        return {"question": question}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while fetching the question: {str(e)}"
        )