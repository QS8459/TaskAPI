from src.core.service.base import AbstractBaseService;
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from sqlalchemy.exc import SQLAlchemyError;
from src.db.models.images.images import Images;
from fastapi import Depends;

class ImagesService(AbstractBaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Images);

    async def addImage(self, **kwargs):
        try:
            with self.session:
                instance = self.model(**kwargs)
                print(instance);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh();
                return instance

        except SQLAlchemyError as e:
            raise e


def get_image_service(session: AsyncSession = Depends(get_async_session)) -> AsyncSession:
    return ImagesService(session);