from fastapi import APIRouter
from app.web.v1.users import users_router
from app.web.v1.questions import questions_router
from app.web.v1.tests import tests_router
from app.web.v1.websockets import websocket_router
from app.web.v1.admin import admin_router


router_v1 = APIRouter(prefix="/v1")
router_v1.include_router(users_router)
router_v1.include_router(questions_router)
router_v1.include_router(tests_router)
router_v1.include_router(websocket_router)
router_v1.include_router(admin_router)
