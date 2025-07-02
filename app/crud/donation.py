from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_open_donations(self, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False  # noqa
            )
        )
        return result.scalars().all()

    async def get_user_donations(
        self,
        session: AsyncSession,
        user_id: int,
    ):
        result = await session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
