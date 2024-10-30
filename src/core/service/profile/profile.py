from src.db.engine import get_async_session;
from src.db.models import Profile;
from src.core.service.base import AbstractBaseService;
from fastapi import Depends;
from pydantic.types import UUID;
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError;
from src.core.schemas.profile import ProfileDetailSchema;
from sqlalchemy.ext.asyncio import AsyncSession;


class ProfileService(AbstractBaseService):
    def __init__(self,session:AsyncSession ):
        super().__init__(session, Profile);

    async def get_profile_by_acc_id(self, owner_id: UUID):
        try:
            async with self.session:
                query = select(self.model).where(self.model.owner == owner_id);
                r = await self.session.execute(query);
                instance = r.scalars().first();
                print(instance)
                if not instance:
                    raise ValueError(f"{self.model.__name__} not found")
                prof = ProfileDetailSchema(
                    id = instance.id,
                    age = instance.age,
                    birth_date = instance.birth_date,
                    instagram = instance.instagram,
                    username = instance.username,
                    facebook = instance.facebook,
                    account = instance.account.to_dict(),
                    about = instance.about,
                    image = instance.image,
                    name = instance.name
                )
                return prof;
        except SQLAlchemyError as e:
            return e

def get_profile_service(session: AsyncSession = Depends(get_async_session)) -> ProfileService:
    return ProfileService(session);
