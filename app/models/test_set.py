from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.hybrid import hybrid_property
from app.database import Base


class TestSet(Base):
    __tablename__ = "test_sets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    source_type = Column(String(10), nullable=False)
    source_content = Column(Text, nullable=False)
    generation_params = Column(JSON, default={})
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    @hybrid_property
    def average_score(self):
        card_averages = [card.average_score for card in self.cards if card.average_score]
        if not card_averages:
            return None
        return sum(card_averages) / len(card_averages)

    cards = relationship("TestCard", back_populates="test_set", cascade="all, delete-orphan")
