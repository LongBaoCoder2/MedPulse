import logging

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.models import Distance, VectorParams

from qllm.core.config import settings

logger = logging.getLogger("uvicorn")


logger = logging.getLogger(__name__)


async def init_qdrant():
    """
    Initialize Qdrant client asynchronously, check if the 'document' collection exists,
    and create it only if it does not exist.
    """
    if settings.QDRANT_API_KEY and settings.QDRANT_URL:
        logger.info("Vector store using Qdrant Cloud")
        client = AsyncQdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    elif not settings.QDRANT_HOST or not settings.QDRANT_PORT:
        raise Exception("Missing Qdrant configuration.")

    else:
        logger.info(
            f"Vector store using local Qdrant: {settings.QDRANT_HOST}:{settings.QDRANT_PORT}"
        )
        client = AsyncQdrantClient(port=settings.QDRANT_PORT, host=settings.QDRANT_HOST)

    # Check if the collection exists
    try:
        await client.get_collection(collection_name="document")
        logger.info("Collection 'document' already exists. Skipping creation.")
    except UnexpectedResponse as e:
        if "404" in str(e):
            # Collection does not exist, create it
            logger.info("Collection 'document' does not exist. Creating it now...")
            await client.create_collection(
                collection_name="document",
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_DIM, distance=Distance.COSINE
                ),
            )
            logger.info("New collection 'document' created.")
        else:
            raise e  # Re-raise other errors

    return client


if __name__ == "__main__":
    # Initialize Qdrant
    import asyncio

    asyncio.run(init_qdrant())
