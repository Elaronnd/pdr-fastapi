from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, BackgroundTasks, Form
from app.db.queries.answers import is_owner_user, edit_answer, get_answer
from app.images.image_check import image_validator
from app.images.image_to_r2 import save_image
from app.schemas.pydantic_answers import AnswerResponse
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user

answers_router = APIRouter(prefix="/answers", tags=["Answers"])


@answers_router.post("/{answer_id}", response_model=AnswerResponse)
async def edit_answer_api(
    answer_id: int,
    background_tasks: BackgroundTasks,
    title: str = Form(default=None, min_length=1, max_length=100),
    image: UploadFile = File(default=None, title="Your image", description="If you want you can upload image of your product"),
    xss_secure: bool = True,
    current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    is_owner = await is_owner_user(answer_id=answer_id, user_id=current_user.id)
    if is_owner is False and current_user.is_admin is False:
        raise HTTPException(status_code=403, detail="You are not owner the answer")


    if image is not None or image != "":
        image_bytes = await image.read()
        await image_validator(image=image, image_bytes=image_bytes)

        image.file.seek(0)
        background_tasks.add_task(save_image, image_bytes=image_bytes, answer_id=answer_id, question_id=None)

    if title is not None or title != '':
        answer_info = await edit_answer(answer_id=answer_id, title=title, xss_secure=xss_secure)
    else:
        answer_info = await get_answer(
            answer_id=answer_id,
            xss_secure=xss_secure
        )
    return AnswerResponse(
        id=answer_info["id"],
        title=answer_info["title"],
        is_right=answer_info["is_right"],
        question_id=answer_info["question_id"]
    )
