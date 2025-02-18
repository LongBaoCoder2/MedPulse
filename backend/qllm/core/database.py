from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from qllm.core.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_async_engine(str(DATABASE_URL))
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
