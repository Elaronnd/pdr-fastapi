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

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'questions': [question.to_dict() for question in self.questions],
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'<Tests(id={self.id}, title={self.title}, description={self.description}), questions={self.questions}, user_id={self.user_id})>'
