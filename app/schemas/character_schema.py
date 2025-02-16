from pydantic import BaseModel, Field, model_validator
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
    house: Optional[str]
    house_id: Optional[int] = None  # Reference to House ID (nullable)
    animal: Optional[str] = Field(None, max_length=50)
    symbol: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    role: str = Field(..., max_length=100)
    age: Optional[int] = Field(None, ge=0)  # Age must be >= 0, can be null
    death: Optional[int] = Field(None, ge=0)  # Death (year) must be >= 0
    strength: Optional[str]
    strength_id: int = Field(..., ge=1)  # Reference to Strength ID

    @model_validator(mode='before')
    def validate_house_fields(cls, values):
        """
        Ensures that:
        1. Only one of `house` or `house_id` is provided.
        2. Only one of `strength` or `strength_id` is provided.
        """
        house = values.get("house")
        house_id = values.get("house_id")

        if house and house_id:
            raise ValueError("Provide either `house` or `house_id`, not both.")

        # Validate `strength` and `strength_id` to ensure only one is provided
        strength = values.get("strength")
        strength_id = values.get("strength_id")

        if strength and strength_id:
            raise ValueError("Provide either `strength` or `strength_id`, not both.")

        return values


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


class CharacterJSONSchema(BaseModel):
    id: Optional[int]
    name: str
    house: Optional[str]
    animal: Optional[str]
    symbol: Optional[str]
    nickname: Optional[str]
    role: Optional[str]
    age: Optional[int]
    death: Optional[int]
    strength: Optional[str]
