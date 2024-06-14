from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine;
from src.config import settings;
from src.db.models.base import AbsModel;

engine = create_async_engine(url = str(settings.pg_uri));
async_session_maker = async_sessionmaker(engine, expire_on_commit=False);

async def get_async_session():
    async with async_session_maker() as session:
        yield session;