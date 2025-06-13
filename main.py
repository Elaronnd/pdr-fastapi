import uvicorn
from app.web.__init__ import app
from app.db.models import *
from app.db.queries.users import register_user
from app.db.base import create_db, drop_db

if __name__ == "__main__":
    drop_db()
    create_db()
    register_user(
        username="admin",
        password="$2b$12$O4v800b1IbjseJWv3tqQsOb19cIMLC/1LtUHy2aChdRIwX0v2B.ki",
        email="admin@admin.com",
        is_admin=True
    ) # password: admin
    uvicorn.run("main:app", reload=True)
