from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from qllm.services.db import SessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None, None]:
    async with SessionLocal() as db:
        yield db
