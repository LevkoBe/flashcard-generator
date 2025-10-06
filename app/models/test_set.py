from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
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

    cards = relationship("TestCard", back_populates="test_set", cascade="all, delete-orphan")
