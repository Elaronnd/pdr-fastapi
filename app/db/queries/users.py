from app.db.base import (
    Session
)

from app.db.models import (
    Users
)

def get_user_by_id(user_id: int):
    with Session() as session:
        user = session.query(Users).filter_by(id = user_id).one_or_none()

        if not user:
            return None
        
        return user.to_dict()