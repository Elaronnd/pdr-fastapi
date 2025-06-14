from typing import Optional
from fastapi import HTTPException, Response
from app.db.queries.tests import get_test_by_id, delete_test


async def delete_test_func(
        test_id: int,
        is_admin: bool,
        user_id: Optional[int] = None
):
    question_info = await get_test_by_id(test_id=test_id)

    if question_info["id"] == user_id or is_admin is True:
        await delete_test(test_id=test_id)
        return Response(status_code=204)

    raise HTTPException(status_code=403, detail="You don't have permission to delete this question")