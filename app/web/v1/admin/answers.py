from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks, Form, UploadFile, File
from app.exceptions import AnswerImageError
from app.images.image_check import image_validator
from app.images.image_to_r2 import save_image
from app.schemas.pydantic_questions import QuestionResponse
from app.services.answers import edit_answer_func
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user

admin_answers_router = APIRouter(prefix="/answers")


@admin_answers_router.post("/", response_model=list[QuestionResponse])
async def edit_answer_admin(
    answer_id: int,
    background_tasks: BackgroundTasks,
    title: Optional[str] = Form(default=None, min_length=1, max_length=100),
    image: Optional[UploadFile] = File(default=None, title="Your image", description="If you want you can upload image of your product"),
    xss_secure: bool = True,
    current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    elif current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not admin")


    elif image is not None or image != "":
        image_bytes = await image.read()
        image_size = (100, 56)
        await image_validator(image=image, image_bytes=image_bytes, image_size=image_size, exception_image_error=AnswerImageError)

        image.file.seek(0)
        background_tasks.add_task(save_image, image_bytes=image_bytes, answer_id=answer_id, question_id=None, folder="answers", image_size=image_size)

    return await edit_answer_func(answer_id=answer_id, title=title, xss_secure=xss_secure)
