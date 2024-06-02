from fastapi import APIRouter;
from .task import router as task_r;
router = APIRouter(prefix = '/v1');

router.include_router(task_r);