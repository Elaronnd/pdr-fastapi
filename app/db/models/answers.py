from app.db.base import Base
from html import escape
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import ForeignKey

class Answers(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    is_right: Mapped[bool] = mapped_column(nullable=False)
    filename: Mapped[str] = mapped_column(nullable=True)

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    user: Mapped['Users'] = relationship(back_populates='answers')

    question: Mapped["Questions"] = relationship(back_populates="answers")

    def to_dict(self, xss_secure: bool = True):
        return {
            "id": self.id,
            "title": self.title if xss_secure is False else escape(self.title),
            "is_right": self.is_right,
            "filename": self.filename,
            "question_id": self.question_id,
            "user_id": self.user_id
        }

    def __repr__(self, xss_secure: bool = True):
        return (
            f"<Answers("
            f"id={self.id}, "
            f"title={self.title if xss_secure is False else escape(self.title)}, "
            f"is_right={self.is_right}, "
            f"filename={self.filename}, "
            f"question_id={self.question_id}, "
            f"user_id={self.user_id}"
            ")>"
        )