from aiocache import cached
from sqlalchemy import select
from app.cache.db.queries import set_cache, delete_cache
from app.db.base import Session
from app.exceptions import AnswerIdError
from app.db.models import Answers
from app.cloud.r2_cloudflare import r2_client


@cached(ttl=60, key="is_owner_answer:{user_id}")
async def is_owner_answer(
    answer_id: int,
    user_id: int
) -> bool:
    async with Session() as session:
        answer = await session.execute(select(Answers).where(Answers.id == answer_id))
        answer = answer.scalar_one_or_none()

        if not answer:
            raise AnswerIdError(message="answer not found", status_code=404, answer_id=answer_id)
        elif answer.user_id != user_id:
            return False
        return True


@cached(ttl=60, key="answer:{answer_id}")
async def get_answer(
    answer_id: int,
    xss_secure: bool = True
):
    async with Session() as session:
        answer = await session.execute(select(Answers).where(Answers.id == answer_id))
        answer = answer.scalar_one_or_none()

        if not answer:
            raise AnswerIdError(message="answer not found", status_code=404, answer_id=answer_id)

        return answer.to_dict(xss_secure=xss_secure)


async def edit_answer(
        answer_id: int,
        title: str = None,
        filename: str = None,
        xss_secure: bool = True
):
    async with Session() as session:
        answer = await session.execute(select(Answers).where(Answers.id == answer_id))
        answer = answer.scalar_one_or_none()

        if not answer:
            raise AnswerIdError(message="answer not found", status_code=404, answer_id=answer_id)
        elif title is not None:
            answer.title = title

        if filename is not None:
            answer.filename = filename

        await session.commit()
        await session.refresh(answer)

        result = answer.to_dict(xss_secure=xss_secure)
        await set_cache(key="answer", cache_id=answer_id, value=result)

        return result


async def delete_answer(
    answer_id: int,
    user_id: int
):
    async with Session() as session:
        answer = await session.execute(select(Answers).where(Answers.id == answer_id))
        answer = answer.scalar_one_or_none()

        if not answer:
            raise AnswerIdError(message="answer not found", status_code=404, answer_id=answer_id)

        if answer.filename is not None:
            await r2_client.delete_file(filename=answer.filename, folder="answers")

        await session.delete(answer)

        await delete_cache(key="answer", cache_id=answer_id)
        await delete_cache(key="is_owner_answer", cache_id=user_id)

        await session.commit()
