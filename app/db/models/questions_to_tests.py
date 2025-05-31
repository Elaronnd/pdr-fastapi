from sqlalchemy import ForeignKey
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class QuestionsToTests(Base):
    __tablename__ = 'questions_to_tests'

    test_id: Mapped[int] = mapped_column(ForeignKey('tests.id'), primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey('questions.id'), primary_key=True)

    position: Mapped[int] = mapped_column(nullable=False)

    tests: Mapped['Tests'] = relationship('Tests', back_populates='test_questions')
    questions: Mapped['Questions'] = relationship('Questions', back_populates='test_questions')

    def to_dict(self):
        return {
            'test_id': self.test_id,
            'question_id': self.question_id,
            'position': self.position
        }

    def __repr__(self):
        return f'<QuestionsToTests(test_id={self.test_id}, question_id={self.question_id}, position={self.position})>'