from fastapi import APIRouter
from app.web.v1.admin.answers import admin_answers_router
from app.web.v1.admin.questions import admin_questions_router
from app.web.v1.admin.tests import admin_tests_router

admin_router = APIRouter(prefix="/admin", tags=["Admin"])
admin_router.include_router(admin_answers_router)
admin_router.include_router(admin_questions_router)
admin_router.include_router(admin_tests_router)
