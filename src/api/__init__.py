from fastapi import APIRouter
from src.api.v1 import api

api_router = APIRouter(prefix="/api")


api_router.include_router(api)
