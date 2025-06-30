from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import auth_backend, fastapi_users
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
users_router.routes = [
    route for route in users_router.routes if route.name != "users:delete_user"
]

router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)


@router.delete("/users/{user_id}", tags=["users"])
async def delete_user(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Пользователь не найден"
        )

    user.is_active = False
    session.add(user)
    await session.commit()

    return
