from src.api.v1.account import account_r;
from src.api.v1.task import task_r;
from src.api.v1.profile.profile import  profile_router;
from src.api.v1.images import router as image_router
from fastapi import APIRouter;

v1_router = APIRouter(prefix = "/v1", tags = ['v']);

v1_router.include_router(account_r);
v1_router.include_router(task_r);
v1_router.include_router(profile_router);
v1_router.include_router(image_router);