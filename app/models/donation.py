from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)

from app.models.base import BaseInvestmentModel


class Donation(BaseInvestmentModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    comment = Column(Text, nullable=True)
