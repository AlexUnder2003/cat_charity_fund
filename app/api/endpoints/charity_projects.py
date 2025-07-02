from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import invest_donations_into_projects
from app.api.validators.charity_project import (
    validate_project_create,
    validate_project_edit,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter(prefix="/charity_project", tags=["charity_project"])


@router.get("/", response_model=list[CharityProjectDB])
async def get_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех благотворительных проектов.
    """
    return await charity_project_crud.get_multi(session)


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создать новый благотворительный проект.

    Только для суперпользователей.
    """
    await validate_project_create(charity_project, session)
    new_project = await charity_project_crud.create(
        charity_project, session, commit=False
    )
    sources = await donation_crud.get_open_donations(session)
    project, updated_donations = invest_donations_into_projects(
        new_project, sources
    )
    session.add(project)
    session.add_all(updated_donations)
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.delete(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    charity_project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Удалить благотворительный проект по ID.

    Только для суперпользователей.
    """
    charity_project_db = await charity_project_crud.get(
        charity_project_id, session
    )
    charity_project = await charity_project_crud.remove(
        charity_project_db,
        session,
    )
    return charity_project


@router.patch(
    "/{charity_project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    charity_project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """
    Частично обновить благотворительный проект по ID.

    Только для суперпользователей.
    """
    charity_project_db = await charity_project_crud.get(
        charity_project_id,
        session,
    )
    await validate_project_edit(
        charity_project_db,
        charity_project_in,
        session,
    )

    updated_project = await charity_project_crud.update(
        charity_project_db, charity_project_in, session, commit=True
    )
    await session.refresh(updated_project)
    return updated_project
