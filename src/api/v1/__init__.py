from src.api.v1.user.user import user_api
from src.api.v1.tasks.tasks import task_api
from fastapi import APIRouter

api = APIRouter(prefix="/v1")

api.include_router(user_api)
api.include_router(task_api)
