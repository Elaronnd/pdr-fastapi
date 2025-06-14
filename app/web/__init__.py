from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.web.v1.__init__ import router_v1
from app.exceptions import (
    UserIdError,
    UsernameError,
    QuestionError,
    QuestionsError,
    QuestionsListError,
    TestError,
    TestsError,
    AnswerIdError,
    AnswerImageError
)


app = FastAPI(
    docs_url="/"
)
app.include_router(router_v1)


@app.exception_handler(UserIdError)
async def user_id_error_handler(request: Request, exception: UserIdError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "user_id": exception.user_id
        },
    )

@app.exception_handler(UsernameError)
async def username_error_handler(request: Request, exception: UsernameError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "username": exception.username
        },
    )


@app.exception_handler(QuestionError)
async def question_error_handler(request: Request, exception: QuestionError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "question_id": exception.question_id
        },
    )


@app.exception_handler(QuestionsError)
async def questions_error_handler(request: Request, exception: QuestionsError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message
        },
    )


@app.exception_handler(QuestionsListError)
async def questions_list_error_handler(request: Request, exception: QuestionsListError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "questions_id": exception.questions_id
        },
    )


@app.exception_handler(TestError)
async def test_error_handler(request: Request, exception: TestError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "test_id": exception.test_id
        },
    )


@app.exception_handler(TestsError)
async def tests_error_handler(request: Request, exception: TestsError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message
        },
    )

@app.exception_handler(AnswerIdError)
async def answer_id_error_handler(request: Request, exception: AnswerIdError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "answer_id": exception.answer_id
        },
    )


@app.exception_handler(AnswerImageError)
async def answer_image_error_handler(request: Request, exception: AnswerImageError):
    return JSONResponse(
        status_code=exception.status_code,
        content={
            "detail": exception.message,
            "filename": exception.filename
        },
    )