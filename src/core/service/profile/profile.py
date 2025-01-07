from src.db.engine import get_async_session;
from src.db.models import Profile;
from src.core.service.base import BaseService;
from fastapi import Depends;
from pydantic.types import UUID;
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError;
from src.core.schemas.profile import ProfileDetailSchema;
from sqlalchemy.ext.asyncio import AsyncSession;


class ProfileService(BaseService):
    def __init__(self,session:AsyncSession ):
        super().__init__(session, Profile);


def get_profile_service(session: AsyncSession = Depends(get_async_session)) -> ProfileService:
    return ProfileService(session);
