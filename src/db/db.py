from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine)
from src.config import settings;
from src.db.models.base import AbstractModel;


engine = create_async_engine(echo = True, future = True, url = str(settings.pg_uri));
async_session = async_sessionmaker(engine, expire_on_commit=False);

async def get_async_session():
    async with async_session() as session:
        yield session