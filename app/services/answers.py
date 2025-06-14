from app.cloud.r2_cloudflare import r2_client
from app.db.queries.answers import edit_answer, get_answer
from app.schemas.pydantic_answers import FullAnswerResponse


async def edit_answer_func(
        answer_id: int,
        title: str = None,
        xss_secure: bool = True
):
    if title:
        answer = await edit_answer(answer_id=answer_id, title=title, xss_secure=xss_secure)
    else:
        answer = await get_answer(
            answer_id=answer_id,
            xss_secure=xss_secure
        )
    return FullAnswerResponse(
        id=answer["id"],
        title=answer["title"],
        is_right=answer["is_right"],
        question_id=answer["question_id"],
        image_url=None if answer["filename"] is None else r2_client.generate_image_url(filename=f"answers/{answer['filename']}")
    )
