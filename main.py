import uvicorn
from app.web.__init__ import app
from app.db.models import *
from app.db.queries.users import register_user
from app.db.queries import create_question_with_answers, create_test_db
from app.db.base import create_db, drop_db
from app.db.check_status import CheckStatus

if __name__ == "__main__":
    drop_db()
    create_db()
    register_user(
        username="admin",
        password="$2b$12$O4v800b1IbjseJWv3tqQsOb19cIMLC/1LtUHy2aChdRIwX0v2B.ki",
        email="admin@admin.com",
        is_admin=True
    ) # password: admin

    create_question_with_answers(
        title="What is the capital of France?",
        user_id=1,
        answers=[
            {"title": "Paris", "is_right": True},
            {"title": "London", "is_right": False},
            {"title": "Berlin", "is_right": False}
        ],
        status=CheckStatus.APPROVED,
        description="A question about the capital of France."
    )

    create_test_db(
        title="Geography Test",
        user_id=1,
        questions_id=[1],
        description="A test about geography, specifically the capital of France.",
        xss_secure=True
    )
    
    uvicorn.run("main:app", reload=True)


# docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.9.0