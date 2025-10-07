from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TestSetBase(BaseModel):
    title: str = Field(..., max_length=255)
    source_type: str = Field(..., pattern="^(text|url)$")
    source_content: str
    generation_params: Optional[Dict[str, Any]] = {}


class TestSetCreate(TestSetBase):
    pass


class TestSetUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)


class TestSetResponse(TestSetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
