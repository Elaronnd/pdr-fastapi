from sqlalchemy import ForeignKey
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

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['Users'] = relationship(back_populates='questions')

    answers: Mapped[list["Answers"]] = relationship(back_populates="question")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'answers': self.answers,
            'user_id': self.user_id,
        }

    def __repr__(self):
        return f'Questions(id={self.id}, title={self.title}, answers={self.answers}), user_id={self.user_id})'
