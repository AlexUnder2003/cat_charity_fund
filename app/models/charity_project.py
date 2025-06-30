from sqlalchemy import Column, String, Text

from app.core.constants import CHARITY_PROJECT_NAME_MAX_LENGTH
from app.models.base import BaseInvestmentModel


class CharityProject(BaseInvestmentModel):
    name = Column(
        String(CHARITY_PROJECT_NAME_MAX_LENGTH), unique=True, nullable=False
    )
    description = Column(Text, nullable=False)
