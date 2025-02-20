from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from qllm.core.config import settings

DATABASE_URL = settings.DATABASE_URL

if "postgresql://" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

print("DATABASE_URL: ", DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
