from contextlib import asynccontextmanager
from typing import Annotated;

from fastapi import FastAPI, Header;
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.config import settings
# from src.dependencies import init_dependencies


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # you can do some initialization here
    yield


def init_routers(_app: FastAPI):
    app.include_router(api_router)


app = FastAPI(
    # title=settings.app_title,
    # description=settings.app_description,
    # version=settings.app_version,
    # lifespan=lifespan,
)
app.include_router(api_router)
# init_dependencies(app)

@app.get('/home')
async def home(user_agent: Annotated[str |None, Header(convert_underscores=False)]= None) :
    from starlette.responses import JSONResponse
    return {"User-Agent": user_agent};

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

