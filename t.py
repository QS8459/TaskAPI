from contextlib import asynccontextmanager;

from fastapi import FastAPI, APIRouter, HTTPException;
from src.api import router;
from starlette.responses import JSONResponse;
app = FastAPI();


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield


app.include_router(router = router);
