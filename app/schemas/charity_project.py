from typing import Optional

from pydantic import BaseModel, Field

from app.core.constants import (
    CHARITY_PROJECT_NAME_MIN_LENGTH,
    CHARITY_PROJECT_NAME_MAX_LENGTH,
    DESCRIPTION_MIN_LENGTH,
)
from app.schemas.base import InvestmentBaseSchema


class CharityProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=CHARITY_PROJECT_NAME_MIN_LENGTH,
        max_length=CHARITY_PROJECT_NAME_MAX_LENGTH,
    )
    description: str = Field(..., min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=CHARITY_PROJECT_NAME_MIN_LENGTH,
        max_length=CHARITY_PROJECT_NAME_MAX_LENGTH,
    )
    description: Optional[str] = Field(None, min_length=DESCRIPTION_MIN_LENGTH)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = "forbid"


class CharityProjectDB(CharityProjectCreate, InvestmentBaseSchema):
    id: int

    class Config:
        orm_mode = True
