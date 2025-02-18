import logging
import os
from datetime import timedelta
from typing import Optional

from cachetools import TTLCache, cached
from fsspec.asyn import AsyncFileSystem
from llama_index.core import StorageContext, VectorStoreIndex, load_index_from_storage
from llama_index.core.callbacks import CallbackManager
from llama_index.core.vector_stores.types import VectorStore
from pydantic import BaseModel, Field

from qllm.core.config import settings

logger = logging.getLogger("uvicorn")

STORAGE_DIR: str = settings.STORAGE_DIR or "storage"


class IndexConfig(BaseModel):
    persist_dir: Optional[str] = Field(
        default=STORAGE_DIR,
    )

    callback_managers: Optional[CallbackManager] = Field(
        default=None,
    )


def get_index(
    vector_store: Optional[VectorStore] = None,
    config: Optional[IndexConfig] = None,
):
    if config is None:
        config = IndexConfig()

    if not os.path.exists(config.persist_dir):
        return None

    logger.info(f"Loading index from {config.persist_dir}...")
    storage_context = get_storage_context(
        persist_dir=None,
        vector_store=vector_store,
    )
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        callback_managers=config.callback_managers,
    )

    logger.info(f"Finished loading index from {config.persist_dir}")
    return index


@cached(
    TTLCache(maxsize=10, ttl=timedelta(minutes=5).total_seconds()),
    key=lambda *args, **kwargs: "global_storage_context",
)
def get_storage_context(
    persist_dir: Optional[str],
    vector_store: Optional[VectorStore],
):
    logger.info("Creating new storage context.")
    return StorageContext.from_defaults(vector_store=vector_store)
