from contextlib import asynccontextmanager
from typing import Annotated;

from fastapi import FastAPI, Header, Depends;
from fastapi.middleware.cors import CORSMiddleware
from src.api import api_router
from src.config import settings

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine


@asynccontextmanager
async def lifespan(_app: FastAPI):
    from src.init_session import engine
    yield
    await engine.dispose()


def init_routers(_app: FastAPI):
    app.include_router(api_router)


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_routers()
