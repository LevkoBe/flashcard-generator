from sqlalchemy import Column, Integer, Float, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("test_cards.id"), nullable=False)
    score = Column(Float, nullable=False)
    user_answer = Column(Text)
    scored_at = Column(TIMESTAMP, server_default=func.now())

    card = relationship("TestCard", back_populates="scores")
