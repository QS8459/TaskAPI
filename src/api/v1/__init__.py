from src.api.v1.account import account_r;
from src.api.v1.task import task_r;
from fastapi import APIRouter;

v1_router = APIRouter(prefix = "/v1", tags = ['v']);

v1_router.include_router(account_r);
v1_router.include_router(task_r);