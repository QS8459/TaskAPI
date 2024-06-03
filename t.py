from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import router
from src.config import settings
from src.dependencies import init_dependencies


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # you can do some initialization here
    yield


def init_routers(_app: FastAPI):
    app.include_router(router)


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(router)
init_dependencies(app)

@app.get('/home')
async def home():
    from starlette.responses import JSONResponse
    return JSONResponse("hello world");

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
