from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Response
)
from app.db.queries.tests import delete_test, get_all_tests
from app.schemas.pydantic_tests import TestResponse, TestCreate
from app.schemas.pydantic_questions import QuestionResponse, FullQuestionResponse
from app.db.queries import (
    get_test_by_id,
    create_test_db,
    get_user_by_username
)
from app.schemas.pydantic_users import UserData
from app.jwt.users import get_current_user

tests_router = APIRouter(prefix="/tests",
                        tags=["Tests"])


@tests_router.post("/", response_model=TestResponse)
async def create_test(
        test: TestCreate,
        current_user: UserData = Depends(get_current_user),
        xss_secure: bool = True
):
    if current_user is None:
        return HTTPException(status_code=403, detail="Not authenticated")
    created_test = await create_test_db(title=test.title, description=test.description, user_id=current_user.id, questions_id=test.questions_id, xss_secure=xss_secure)
    return TestResponse(
        id=created_test["id"],
        title=created_test["title"],
        description=created_test["description"],
        questions=created_test["questions"],
        user_id=created_test["user_id"]
    )


@tests_router.get("/", response_model=list[TestResponse])
async def get_all_tests_api(
    xss_secure: bool = True
):
    tests = await get_all_tests(xss_secure=xss_secure)
    return [
        TestResponse(
            id=test["id"],
            title=test["title"],
            description=test["description"],
            questions=[
                QuestionResponse(
                    id=question["id"],
                    title=question["title"],
                    user_id=question["user_id"],
                    answers=question["answers"]
                )
                for question in test["questions"]
            ],
            user_id=test["user_id"]
        )
        for test in tests
    ]


@tests_router.delete("/{test_id}")
async def delete_test_api(
        test_id: int,
        current_user: UserData = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    user_data = await get_user_by_username(username=current_user.username)
    user_tests = user_data.get("tests", [])

    if any(test.get("id") == test_id for test in user_tests) or current_user.is_admin is True:
        await delete_test(test_id=test_id)
        return Response(status_code=204)

    raise HTTPException(status_code=403, detail="You don't have permission to delete this question")


@tests_router.get("/{test_id}", response_model=TestResponse)
async def get_test(
        test_id: int,
        xss_secure: bool = True
):
    test = await get_test_by_id(test_id=test_id, xss_secure=xss_secure)

    return TestResponse(
        id=test["id"],
        title=test["title"],
        description=test["description"],
        questions=[
            FullQuestionResponse(
                id=question["id"],
                title=question["title"],
                user_id=question["user_id"],
                answers=question["answers"],
                tests_count=question["test_count"],
                status=question["status"]
            )
            for question in test["questions"]
        ],
        user_id=test["user_id"]
    )
