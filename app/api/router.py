from fastapi import APIRouter

from app.api.endpoints import (
    charity_project_router,
    donation_router,
    user_router,
)

router = APIRouter()
router.include_router(user_router)
router.include_router(donation_router)
router.include_router(charity_project_router)
