from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Form, UploadFile, File
from app.cloud.r2_cloudflare import r2_client
from app.db.check_status import CheckStatus
from app.exceptions import QuestionImageError
from app.images.image_check import image_validator
from app.images.image_to_r2 import save_image
from app.schemas.pydantic_answers import FullAnswerInQuestionResponse
from app.schemas.pydantic_questions import FullQuestionResponse, QuestionResponse
from app.services.questions import get_question_func, edit_question_func, delete_question_func
from app.web.v1.questions import get_all_questions_func
from app.db.queries import edit_status_question
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user

admin_questions_router = APIRouter(prefix="/questions")


@admin_questions_router.post("/status/{question_id}", response_model=FullQuestionResponse)
async def change_status_question(
    question_id: int,
    status: CheckStatus,
    xss_secure: bool = True,
    current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")
    question = await edit_status_question(
        question_id=question_id,
        status=status,
        xss_secure=xss_secure
    )
    return FullQuestionResponse(
        id=question["id"],
        title=question["title"],
        user_id=question["user_id"],
        answers=[
            FullAnswerInQuestionResponse(
                id=answer["id"],
                title=answer["title"],
                is_right=answer["is_right"],
                image_url=None if answer["filename"] is None else r2_client.generate_image_url(filename=f"answers/{answer['filename']}")
            ) for answer in question["answers"]
        ],
        status=question["status"]
    )

@admin_questions_router.get("/", response_model=list[QuestionResponse])
async def get_questions_admin(
        xss_secure: bool = True,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")
    return await get_all_questions_func(is_admin=True, xss_secure=xss_secure)


@admin_questions_router.get("/{question_id}", response_model=FullQuestionResponse)
async def get_question_admin(
        question_id: int,
        xss_secure: bool = True,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")
    return await get_question_func(is_admin=True, xss_secure=xss_secure, question_id=question_id)


@admin_questions_router.post("/{question_id}", response_model=QuestionResponse)
async def edit_question_admin(
        question_id: int,
        background_tasks: BackgroundTasks,
        title: Optional[str] = Form(default=None, min_length=1, max_length=100),
        description: Optional[str] = Form(default=None, title="Description", min_length=1, max_length=500,
                                          description="Description of the test"),
        image: Optional[UploadFile] = File(default=None, title="Your image",
                                           description="If you want you can upload image of your product"),
        xss_secure: bool = True,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")

    elif image is not None or image != "":
        image_bytes = await image.read()
        image_size = (500, 500)
        await image_validator(image=image, image_bytes=image_bytes, image_size=image_size, exception_image_error=QuestionImageError)

        image.file.seek(0)
        background_tasks.add_task(save_image, image_bytes=image_bytes, answer_id=None, question_id=question_id, folder="questions", image_size=image_size)

    return await edit_question_func(question_id=question_id, is_admin=True, title=title, description=description, xss_secure=xss_secure)


@admin_questions_router.delete("/{question_id}")
async def delete_question_admin(
        question_id: int,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")

    return await delete_question_func(question_id=question_id, is_admin=True)
