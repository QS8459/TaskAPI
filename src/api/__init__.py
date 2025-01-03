from fastapi import APIRouter;
from src.api.v1 import v1_router;
api_router = APIRouter(prefix = "/api", tags = ['api']);


api_router.include_router(v1_router);