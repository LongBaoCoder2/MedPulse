import logging
from typing import Annotated, AsyncGenerator, Generator

from fastapi import Depends
from llama_index.core.vector_stores.types import VectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient, QdrantClient
from sqlalchemy.ext.asyncio import AsyncSession

from qllm.core.database import async_session_maker
from qllm.core.vector_store import get_vector_store

logger = logging.getLogger("uvicorn")


def get_qdrant_vector_store() -> VectorStore:
    """
    Dependency to provide QdrantVectorStore.
    """
    return get_vector_store()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
