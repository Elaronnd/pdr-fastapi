from fastapi import (
    APIRouter,
    HTTPException
)

from app.db.queries import (
    get_test_by_id
)

tests_router = APIRouter(prefix="/tests",
                        tags=["Тести 📜"])

@tests_router.get("/{test_id}")
async def get_test(test_id: int):
    
    test = get_test_by_id(test_id)

    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    
    return test



