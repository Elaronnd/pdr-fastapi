from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, UploadFile, File, Form
from app.db.queries.questions import is_owner_user
from app.db.queries.users import get_user_by_username
from app.exceptions import QuestionImageError
from app.images.image_check import image_validator
from app.images.image_to_r2 import save_image
from app.schemas.pydantic_questions import (
    QuestionCreate,
    QuestionResponse,
    FullQuestionResponse
)
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user
from app.services.questions import get_all_questions_func, get_question_func, edit_question_func, delete_question_func, add_question_func

questions_router = APIRouter(prefix="/questions", tags=["Questions"])


@questions_router.post("/", response_model=QuestionResponse)
async def add_question(
    question: QuestionCreate,
    current_user: UserData = Depends(get_current_user),
    xss_secure: bool = True
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return await add_question_func(question=question, is_admin=False, user_id=current_user.id, xss_secure=xss_secure)


@questions_router.post("/{question_id}", response_model=FullQuestionResponse)
async def edit_question_api(
        question_id: int,
        background_tasks: BackgroundTasks,
        title: Optional[str] = Form(default=None, min_length=1, max_length=100),
        description: Optional[str] = Form(default=None, title="Description", min_length=1, max_length=500, description="Description of the question"),
        image: Optional[UploadFile] = File(default=None, title="Your image", description="If you want you can upload image of your question"),
        xss_secure: bool = True,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    is_owner = await is_owner_user(question_id=question_id, user_id=current_user.id)
    if is_owner is False and current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not owner the answer")

    elif image is not None or image != "":
        image_bytes = await image.read()
        image_size = (500, 500)
        await image_validator(image=image, image_bytes=image_bytes, image_size=image_size, exception_image_error=QuestionImageError)

        image.file.seek(0)
        background_tasks.add_task(save_image, image_bytes=image_bytes, answer_id=None, question_id=question_id, folder="questions", image_size=image_size)

    return await edit_question_func(question_id=question_id, is_admin=False, title=title, description=description, xss_secure=xss_secure)


@questions_router.delete("/{question_id}")
async def delete_question_api(
        question_id: int,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")

    return await delete_question_func(question_id=question_id, is_admin=False, user_id=current_user.id)


@questions_router.get("/", response_model=list[QuestionResponse])
async def get_all_questions_api(xss_secure: bool = True):
    return await get_all_questions_func(is_admin=False, xss_secure=xss_secure)


@questions_router.get("/{question_id}", response_model=FullQuestionResponse)
async def get_question_by_id_api(question_id: int, xss_secure: bool = True, current_user: UserData = Depends(get_current_user)):
    return await get_question_func(question_id=question_id, xss_secure=xss_secure, user_id=current_user.id, is_admin=False)
