from fastapi import FastAPI
from app.web.v1.__init__ import router_v1


app = FastAPI(
    docs_url="/"
)
app.include_router(router_v1)
