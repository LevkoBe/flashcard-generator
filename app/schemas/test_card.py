from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator


class TestCardBase(BaseModel):
    front_side: str
    back_side: str
    position: int = 0

    @field_validator("front_side", "back_side")
    @classmethod
    def validate_word_count(cls, v: str) -> str:
        word_count = len(v.split())
        if word_count > 50:
            raise ValueError(f"Must be ≤50 words (got {word_count})")
        return v


class TestCardCreate(TestCardBase):
    pass


class TestCardUpdate(BaseModel):
    front_side: Optional[str] = None
    back_side: Optional[str] = None
    position: Optional[int] = None

    @field_validator("front_side", "back_side")
    @classmethod
    def validate_word_count(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            word_count = len(v.split())
            if word_count > 50:
                raise ValueError(f"Must be ≤50 words (got {word_count})")
        return v


class TestCardResponse(TestCardBase):
    id: int
    test_set_id: int
    created_at: datetime
    average_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
