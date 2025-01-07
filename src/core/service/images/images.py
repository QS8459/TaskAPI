from src.core.service.base import BaseService;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.exc import SQLAlchemyError;
from src.db.models.images.images import Images;
from fastapi import Depends;

class ImagesService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Images);


def get_image_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return ImagesService(session);