from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.base import InvestmentBaseSchema


class DonationCreate(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str]


class DonationDBUser(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBFull(DonationCreate, InvestmentBaseSchema):
    id: int
    user_id: int

    class Config:
        orm_mode = True
