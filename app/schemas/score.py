from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScoreCreate(BaseModel):
    user_answer: str


class ScoreResponse(BaseModel):
    id: int
    card_id: int
    score: float = Field(..., ge=0.0, le=1.0)
    user_answer: Optional[str] = None
    scored_at: datetime

    class Config:
        from_attributes = True


class ScoreResult(BaseModel):
    score: float
    correct: bool
    expected: str
