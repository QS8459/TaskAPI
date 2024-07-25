from fastapi import Depends;
from sqlalchemy.future import select;
from sqlalchemy.exc import SQLAlchemyError
from src.db.engine import get_async_session;
from sqlalchemy.ext.asyncio import AsyncSession;
from src.core.service.base import AbstractBaseService;
from src.db.models.verification_code.verification_code import Verification_Code;


from random import randint, seed;
from datetime import datetime, timedelta;
from time import time;
seed(time());

class VerificationService(AbstractBaseService):
    def __init__(self, session):
        super().__init__(session, Verification_Code);

    async def generate_code(self, email, user_id):
        try:
            async with self.session:
                random_number = randint(000000,999_999);
                instance = self.model(verification_code = random_number,code_for = user_id);
                self.session.add(instance);
                await self.session.commit();
                await self.session.refresh(instance);
                print("The verification code: ",instance.verify_code);
                return instance
        except SQLAlchemyError as e:
            raise e;
    async def verify_user(self,user_id):
        try:
            async with self.session:
                super().get_and_update(user_id)
                result = await self.session.execute();
                instance = result.scalars().first();
                if not instance:
                    raise ValueError(f"{self.model.__name__} not found");
                return {"detail":"success", "status": 200, "user_id": instance.code_for};
        except SQLAlchemyError as e:
            raise e

async def v_code_service(session:AsyncSession = Depends(get_async_session)):
    return VerificationService(session)