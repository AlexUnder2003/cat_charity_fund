from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.init import create_first_superuser
from app.api.router import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_first_superuser()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router)
