import os
from datetime import timedelta
from typing import Optional

from cachetools import TTLCache, cached
from llama_index.core import SimpleDirectoryReader, load_index_from_storage
from llama_index.core.storage import StorageContext
from llama_index.core.vector_stores.types import VectorStore
from qdrant_client import QdrantClient


@cached(
    TTLCache(maxsize=10, ttl=timedelta(minutes=5).total_seconds()),
    key=lambda *args, **kwargs: "global_storage_context",
)
def get_storage_context(
    persist_dir: Optional[str],
    vector_store: Optional[VectorStore],
):
    return StorageContext.from_defaults(
        persist_dir=persist_dir, vector_store=vector_store
    )


def get_index(
    persist_dir: Optional[str] = None,
    vector_store: Optional[VectorStore] = None,
):
    if not os.path.exists(persist_dir):
        persist_dir = None

    storage_context = get_storage_context(
        persist_dir=None,
        vector_store=vector_store,
    )
    index = load_index_from_storage(
        storage_context=storage_context,
    )
    return index


def insert_into_index(index, filepath):
    try:
        documents = SimpleDirectoryReader(filepath).load_data()[0]

        index.insert(documents)
        print(f"Document inserted and index persisted successfully.")
    except Exception as e:
        print(f"Error during document insertion: {e}", exc_info=True)


def main():
    from llama_index.core import VectorStoreIndex
    from llama_index.vector_stores.qdrant import QdrantVectorStore

    documents = SimpleDirectoryReader("./data/").load_data()

    client = QdrantClient(host="localhost", port=6333)
    vector_store = QdrantVectorStore(
        "document",
        client=client,
        batch_size=20,
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    index.storage_context.persist("/storage")

    print("Successfully.")


if __name__ == "__main__":
    main()
