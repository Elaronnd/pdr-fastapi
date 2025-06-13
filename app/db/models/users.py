from html import escape
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
    is_admin: Mapped[bool] = mapped_column(nullable=False)

    questions: Mapped[list['Questions']] = relationship(back_populates='user')
    tests: Mapped[list['Tests']] = relationship(back_populates='user')
    answers: Mapped[list['Answers']] = relationship(back_populates='user')

    def to_dict(self, xss_secure: bool = True):
        return {
            'id': self.id,
            'username': self.username if xss_secure is False else escape(self.username),
            'email': self.email if xss_secure is False else escape(self.email),
            'password': self.password,
            'questions': [question.to_dict(xss_secure=xss_secure) for question in self.questions],
            'tests': [test.to_dict(xss_secure=xss_secure) for test in self.tests],
            'is_admin': self.is_admin
        }

    def __repr__(self):
        return (
            f'<Users('
            f'id={self.id}, '
            f'username={self.username}, '
            f'email={self.email}), '
            f'password={self.password}), '
            f'questions={self.questions}), '
            f'tests={self.tests}, '
            f'is_admin={self.is_admin}'
            f')>'
        )
