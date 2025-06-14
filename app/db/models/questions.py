from html import escape
from app.db.check_status import CheckStatus
from sqlalchemy import ForeignKey, Enum
from app.db.base import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)


class Questions(Base):
    __tablename__ = 'questions'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[CheckStatus] = mapped_column(Enum(CheckStatus), nullable=False, default=CheckStatus.PENDING)
    filename: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['Users'] = relationship(back_populates='questions')

    test_questions: Mapped[list['QuestionsToTests']] = relationship(back_populates='questions')
    tests: Mapped[list['Tests']] = relationship(
        'Tests',
        secondary='questions_to_tests',
        viewonly=True,
        back_populates='questions',
        cascade="all, delete-orphan"
    )
    answers: Mapped[list["Answers"]] = relationship(back_populates="question", cascade="all, save-update, delete, delete-orphan")

    def to_dict(self, xss_secure: bool = True):
        return {
            'id': self.id,
            'title': escape(self.title) if xss_secure else self.title,
            'description': escape(self.description) if xss_secure else self.description,
            'user_id': self.user_id,
            'status': self.status,
            'answers': [answer.to_dict(xss_secure=xss_secure) for answer in self.answers],
            'test_count': len(self.test_questions)
        }

    def __repr__(self):
        return (
            f'<Questions('
            f'id={self.id}, '
            f'title={escape(self.title)}, '
            f'description={escape(self.description)}, '
            f'answers={self.answers}, '
            f'user_id={self.user_id}, '
            f'status={self.status}, '
            f'test_count={len(self.test_questions)}'
            ')>'
        )
