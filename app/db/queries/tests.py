from app.db.base import (
    Session
)

from app.db.models import (
    Tests
)

def get_test_by_id(test_id: int):
    with Session() as session:
        test = session.query(Tests).filter_by(id=test_id).one_or_none()

        if not test:
            return None
        
        return test.to_dict()