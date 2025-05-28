import uvicorn
from app.web.__init__ import app
from app.db.models import *
from app.db.base import create_db, drop_db

if __name__ == "__main__":
    drop_db()
    create_db()
    uvicorn.run("main:app", reload=True)
