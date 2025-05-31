from app.db.base import Base

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import ForeignKey

class Answers(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    is_right: Mapped[bool] = mapped_column(nullable=False)

    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    question: Mapped["Questions"] = relationship(back_populates="answers")

    def to_dict(self):
        return {
            "id": self.id,
            "is_right": self.is_right,
            "question_id": self.question_id,
        }

    def __repr__(self):
        return f"<Answers(id={self.id}, is_right={self.is_right}, question_id={self.question_id})>"