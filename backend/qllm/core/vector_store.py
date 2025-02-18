import logging

from llama_index.core.vector_stores.types import VectorStore
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import AsyncQdrantClient, QdrantClient

from qllm.core.config import settings
from qllm.services.qdrant_service import init_qdrant

logger = logging.getLogger("uvicorn")

init_index = False
singleton_vector_store = None


def get_vector_store() -> VectorStore:
    global singleton_vector_store
    if singleton_vector_store is not None:
        return singleton_vector_store

    if settings.QDRANT_URL is not None and settings.QDRANT_API_KEY is not None:
        logger.info("Use Qdrant cloud - https://cloud.qdrant.io/.")
        aclient = AsyncQdrantClient(
            url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY
        )
        client = QdrantClient(url=settings.QDRANT_URL, api_key=settings.QDRANT_API_KEY)
    else:
        logger.info(
            f"Use local Qdrant on host: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
        )
        aclient = AsyncQdrantClient(
            host=settings.QDRANT_HOST, port=settings.QDRANT_PORT
        )
        client = QdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

    singleton_vector_store = QdrantVectorStore(
        client=client,
        aclient=aclient,
        collection_name=settings.COLLECTION_NAME,
    )

    return singleton_vector_store


async def run_init_vector_store():
    global init_index
    if init_index:
        return

    if singleton_vector_store is None:
        raise Exception(
            "Vector store is not initialized. Please try initializing before init collection."
        )

    await init_qdrant()
    init_index = True
