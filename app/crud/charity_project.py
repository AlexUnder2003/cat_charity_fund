from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CharityProjectCRUD(CRUDBase):
    async def get_by_name(self, name: str, session: AsyncSession):
        result = await session.execute(
            select(self.model).where(self.model.name == name)
        )
        return result.scalars().first()

    async def get_open_projects(self, session: AsyncSession):
        result = await session.execute(
<<<<<<< HEAD
            select(self.model).where(self.model.fully_invested is False)
=======
            select(self.model).where(self.model.fully_invested == False)
>>>>>>> 0f8cca6 (Update investments logic and improve code readbility)
        )
        return result.scalars().all()

    async def remove(
        self,
        db_obj,
        session: AsyncSession,
    ):
        if db_obj.invested_amount > 0:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail="Нельзя удалить проект с инвестициями.",
            )

        await session.delete(db_obj)
        await session.commit()
        return db_obj


charity_project_crud = CharityProjectCRUD(CharityProject)
