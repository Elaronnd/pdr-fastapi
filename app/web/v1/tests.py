from fastapi import (
    APIRouter,
    HTTPException
)
from app.schemas.pydantic_tests import TestResponse
from app.db.queries import (
    get_test_by_id
)

tests_router = APIRouter(prefix="/tests",
                        tags=["Tests"])

@tests_router.get("/{test_id}", response_model=TestResponse)
async def get_test(test_id: int, xss_secure: bool = True):
    test = get_test_by_id(test_id=test_id, xss_secure=xss_secure)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")

    return TestResponse(
        id=test.get("id"),
        title=test.get("title"),
        description=test.get("description"),
        questions=test.get("questions"),
        user_id=test.get("user_id")
    )
