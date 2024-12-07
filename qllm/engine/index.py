import logging
import os
from datetime import timedelta
from typing import Optional

from cachetools import TTLCache, cached
from fsspec.asyn import AsyncFileSystem
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.callbacks import CallbackManager
from llama_index.core.vector_stores.types import VectorStore
from pydantic import BaseModel, Field

logger = logging.getLogger("uvicorn")


class IndexConfig(BaseModel):
    callback_managers: Optional[CallbackManager] = Field(
        default=None,
    )


def get_index_from_disk(config: IndexConfig | None = None):
    if config is None:
        config = IndexConfig()

    storage_dir = os.getenv("STORAGE_DIR", "storage")
    if not os.path.exists(storage_dir):
        return None

    logger.info(f"Loading index from {storage_dir}...")
    storage_context = get_storage_context(storage_dir)
    index = load_index_from_storage(
        storage_context=storage_context,
        callback_manager=config.callback_manager,
    )
    logger.info(f"Finished loading index from {storage_dir}")
    return index


@cached(
    TTLCache(maxsize=10, ttl=timedelta(minutes=5).total_seconds()),
    key=lambda *args, **kwargs: "global_storage_context",
)
def get_storage_context(
    persist_dir: Optional[str],
    vector_store: Optional[VectorStore],
    fs: Optional[AsyncFileSystem],
):
    logger.info("Creating new storage context.")
    return StorageContext.from_defaults(
        persist_dir=persist_dir, vector_store=vector_store, fs=fs
    )
