from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.config import settings
from src.logger import log
from src.custom_middleware import logger
@asynccontextmanager
async def lifespan(_app: FastAPI):
    log.info("Initializing db connections")
    from src.init_session import engine
    yield
    await engine.dispose()


def init_routers(_app: FastAPI):
    log.info("INITIALIZING ROUTES")
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
app.middleware('http')(logger)

init_routers(app)
