from src.config import settings
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

engine: AsyncEngine = create_async_engine(str(settings.pg_uri))
async_session_maker: async_sessionmaker = async_sessionmaker(engine, expire_on_commit = False)