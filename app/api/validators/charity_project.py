from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def validate_project_create(
    project: CharityProject,
    session: AsyncSession,
):
    if await charity_project_crud.get_by_name(project.name, session):
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "Проект с таким именем уже существует",
        )

    return


async def validate_project_edit(
    project: CharityProject, data: CharityProjectUpdate, session: AsyncSession
):
    if project.fully_invested:
        raise HTTPException(
            HTTPStatus.BAD_REQUEST,
            "Проект закрыт и не подлежит редактированию.",
        )

    if data.name and data.name != project.name:
        existing_project = await charity_project_crud.get_by_name(
            data.name, session
        )
        if existing_project:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Проект с таким именем уже существует.",
            )

    if data.full_amount:
        if data.full_amount < project.invested_amount:
            raise HTTPException(
                HTTPStatus.BAD_REQUEST,
                "Нельзя установить сумму меньше уже инвестированной.",
            )
