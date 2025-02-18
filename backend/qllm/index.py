import logging
import os
from multiprocessing import Lock
from multiprocessing.managers import BaseManager

from llama_index.core import (
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.schema import QueryType

from qllm.core.config import configure_logging

configure_logging()

index_lock = Lock()
index: VectorStoreIndex | None = None


def initialize_index():
    global index, index_lock

    index_dir = "./.index"
    document_dir = "./documents"

    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    with index_lock:
        try:
            if os.path.exists(index_dir):
                logging.info("Index directory exists. Loading index from storage.")
                index = load_index_from_storage(storage_context)
            else:
                logging.info("Index directory not found. Creating a new index.")
                dir_reader = SimpleDirectoryReader(document_dir)
                documents = dir_reader.load_data()

                index = VectorStoreIndex.from_documents(
                    documents=documents, storage_context=storage_context
                )
                index.storage_context.persist(index_dir)
                logging.info("Index created and persisted successfully.")
        except Exception as e:
            logging.error(f"Error during index initialization: {e}", exc_info=True)


def query_index(query_text: QueryType) -> RESPONSE_TYPE:
    global index

    try:
        logging.info(f"Executing query: {query_text}")
        query_engine = index.as_query_engine()
        queried_text = query_engine.query(query_text)
        logging.info(f"Query executed successfully.")
        return queried_text
    except Exception as e:
        logging.error(f"Error during query execution: {e}", exc_info=True)
        raise


def insert_into_index(filepath, doc_id: str | None = None):
    global index, index_lock

    try:
        logging.info(f"Inserting document from: {filepath} with doc_id: {doc_id}")
        documents = SimpleDirectoryReader(filepath).load_data()[0]
        if doc_id is not None:
            documents.doc_id = doc_id

        with index_lock:
            index.insert(documents)
            index.storage_context.persist()
            logging.info(f"Document inserted and index persisted successfully.")
    except Exception as e:
        logging.error(f"Error during document insertion: {e}", exc_info=True)


if __name__ == "__main__":
    try:
        logging.info("Starting application.")
        initialize_index()

        manager = BaseManager(("127.0.0.1", 5602), b"Password")
        manager.register("query_index", query_index)
        manager.register("insert_into_index", insert_into_index)
        server = manager.get_server()

        logging.info("Server started. Waiting for connections.")
        server.serve_forever()
    except Exception as e:
        logging.critical(f"Critical error in main process: {e}", exc_info=True)
