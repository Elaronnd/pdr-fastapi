from app.db.base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    questions: Mapped[list['Questions']] = relationship(back_populates='users')
    tests: Mapped[list['Tests']] = relationship(back_populates='users')

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'questions': [question.to_dict() for question in self.questions],
            'tests': [test.to_dict() for test in self.tests]
        }

    def __repr__(self):
        return f'Users(id={self.id}, username={self.username}, email={self.email}), password={self.password}), questions={self.questions}), tests={self.tests}'
