from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils import invest_donations_into_projects
from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDBFull, DonationDBUser

router = APIRouter(prefix="/donation", tags=["donations"])


@router.get(
    "/",
    response_model=list[DonationDBFull],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)

    return donations


@router.post("/", response_model=DonationDBUser)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user, commit=False
    )
    sources = await charity_project_crud.get_open_projects(session)
    donation, updated_projects = invest_donations_into_projects(
        new_donation, sources
    )
    session.add(donation)
    session.add_all(updated_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation


@router.get(
    "/my",
    response_model=list[DonationDBUser],
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_user_donations(session, user.id)
    return donations
