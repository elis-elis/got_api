from pydantic import BaseModel, Field
from typing import Optional


class HouseCreateSchema(BaseModel):
    """
    Schema for creating a new house. Contains the name of the house.
    """
    name: str = Field(..., max_length=50)


class HouseResponseSchema(BaseModel):
    """
    Schema for returning house details with ID and name.
    """
    id: int
    name: str = Field(..., max_length=50)


class StrengthCreateSchema(BaseModel):
    """
    Schema for creating a new strength. Contains the description of the strength.
    """
    description: str = Field(..., max_length=50)


class StrengthResponseSchema(BaseModel):
    """
    Schema for returning strength details with ID and description.
    """
    id: int
    description: str = Field(..., max_length=50)


class CharacterCreateSchema(BaseModel):
    """
    Schema for creating a new character. Includes name, house, strength, and other attributes.
    """
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
    """
    Schema for returning a character's details, including full house and strength info.
    """
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


class CharacterUpdateSchema(BaseModel):
    """
    Schema for updating character details. Allows modification of character attributes.
    """
    name: Optional[str] = Field(None, max_length=100)
    house_id: Optional[int] = None
    animal: Optional[str] = Field(None, max_length=50)
    symbol: Optional[str] = Field(None, max_length=50)
    nickname: Optional[str] = Field(None, max_length=50)
    role: Optional[str] = Field(None, max_length=100)
    age: Optional[int] = Field(None, ge=0)
    death: Optional[int] = Field(None, ge=0)
    strength_id: Optional[int] = Field(None, ge=1)

    class Config:
        extra = "forbid"  # Prevents users from sending unexpected fields


class CharacterJSONSchema(BaseModel):
    """
    Schema for accepting character data in JSON format (without ID and full details).
    """
    name: str
    house: Optional[str]
    animal: Optional[str]
    symbol: Optional[str]
    nickname: Optional[str]
    role: Optional[str]
    age: Optional[int]
    death: Optional[int]
    strength: Optional[str]
