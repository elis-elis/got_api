from pydantic import BaseModel, Field
from typing import Optional


class CharacterSchema(BaseModel):
    name: str = Field(..., max_length=100)
    house: Optional[str] = Field(None, max_length=50)
    animal: Optional[str] = Field(None, max_length=50)
    symbol: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    role: str = Field(..., max_length=100)
    age: Optional[int] = Field(None, ge=0)  # Age must be >= 0
    death: Optional[int] = Field(None, ge=0)  # Death (year) must be >= 0
    strength: str = Field(..., max_length=100)
