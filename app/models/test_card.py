from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class TestCard(Base):
    __tablename__ = "test_cards"

    id = Column(Integer, primary_key=True, index=True)
    test_set_id = Column(Integer, ForeignKey("test_sets.id"), nullable=False)
    front_side = Column(Text, nullable=False)
    back_side = Column(Text, nullable=False)
    position = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.now())

    test_set = relationship("TestSet", back_populates="cards")
    scores = relationship("Score", back_populates="card", cascade="all, delete-orphan")
