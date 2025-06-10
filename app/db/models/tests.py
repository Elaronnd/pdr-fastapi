from html import escape
from sqlalchemy import ForeignKey
from app.db.base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)


class Tests(Base):
    __tablename__ = 'tests'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    test_questions: Mapped[list['QuestionsToTests']] = relationship(back_populates='tests')
    questions: Mapped[list['Questions']] = relationship(
        'Questions',
        secondary='questions_to_tests',
        viewonly=True,
        back_populates='tests'
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['Users'] = relationship(back_populates='tests')

    def to_dict(self, xss_secure: bool = True):
        return {
            'id': self.id,
            'title': escape(self.title) if xss_secure else self.title,
            'description': escape(self.description) if xss_secure else self.description,
            'questions': [question.to_dict(xss_secure=xss_secure) for question in self.questions],
            'user_id': self.user_id,
        }

    def __repr__(self):
        return (
            f'<Tests('
            f'id={self.id}, '
            f'title={self.title}, '
            f'description={self.description}), '
            f'questions={self.questions}, '
            f'user_id={self.user_id})>'
        )
