from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class InvestmentBaseSchema(BaseModel):
    full_amount: int = Field(
        ..., gt=0, description="Требуемая/пожертвованная сумма"
    )
    invested_amount: Optional[int] = Field(
        0, ge=0, description="Уже инвестированная сумма"
    )
    fully_invested: Optional[bool] = Field(
        False, description="Закрыта ли инвестиция"
    )
    create_date: datetime
    close_date: Optional[datetime] = None
