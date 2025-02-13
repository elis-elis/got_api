from pydantic import BaseModel, Field
from typing import Optional


class HouseCreateSchema(BaseModel):
    name: str = Field(..., max_length=50)


class HouseResponseSchema(BaseModel):
    id: int
    name: str = Field(..., max_length=50)


class StrengthCreateSchema(BaseModel):
    description: str = Field(..., max_length=50)


class StrengthResponseSchema(BaseModel):
    id: int
    description: str = Field(..., max_length=50)


class CharacterCreateSchema(BaseModel):
    name: str = Field(..., max_length=100)
    house_id: Optional[int] = None  # Reference to House ID (nullable)
    animal: Optional[str] = Field(None, max_length=50)
    symbol: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    role: str = Field(..., max_length=100)
    age: Optional[int] = Field(None, ge=0)  # Age must be >= 0, can be null
    death: Optional[int] = Field(None, ge=0)  # Death (year) must be >= 0
    strength_id: int = Field(..., ge=1)  # Reference to Strength ID


# Schema for returning a character (Includes ID + full house and strength details)
class CharacterResponseSchema(BaseModel):
    id: int
    name: str
    house: Optional[HouseResponseSchema] = None
    animal: Optional[str] = None
    symbol: Optional[str] = None
    nickname: Optional[str] = None
    role: str
    age: Optional[int] = None
    death: Optional[int] = None
    strength: StrengthResponseSchema
