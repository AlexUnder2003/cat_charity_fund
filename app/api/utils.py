from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def invest_donations_into_projects(session: AsyncSession):
    projects_result = await session.execute(
        select(CharityProject)
        .where(CharityProject.fully_invested == 0)
        .order_by(CharityProject.create_date)
    )
    donations_result = await session.execute(
        select(Donation)
        .where(Donation.fully_invested == 0)
        .order_by(Donation.create_date)
    )

    projects = projects_result.scalars().all()
    donations = donations_result.scalars().all()

    now = datetime.now(timezone.utc)

    for project in projects:
        project_left = project.full_amount - project.invested_amount

        for donation in donations:
            donation_left = donation.full_amount - donation.invested_amount

            invest_amount = min(project_left, donation_left)

            project.invested_amount += invest_amount
            donation.invested_amount += invest_amount

            if project.invested_amount == project.full_amount:
                project.fully_invested = True
                project.close_date = now

            if donation.invested_amount == donation.full_amount:
                donation.fully_invested = True
                donation.close_date = now

    session.add_all(projects + donations)
