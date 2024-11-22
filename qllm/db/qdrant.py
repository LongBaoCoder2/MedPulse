from qdrant_client import QdrantClient

from qllm.core import VectorDBManager


class QdrantManager(VectorDBManager):
    def initialize(self, host="localhost", port=6333):
        self.client = QdrantClient(host=host, port=port)
        self.collection_name = "example_collection"
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config={"size": 512, "distance": "Cosine"},
        )

    def insert_vectors(self, vectors):
        payload = [
            {"id": v["id"], "vector": v["values"], "payload": v["metadata"]}
            for v in vectors
        ]
        self.client.upsert(collection_name=self.collection_name, points=payload)

    def query_vectors(self, vector, top_k=5):
        results = self.client.search(
            collection_name=self.collection_name, vector=vector, limit=top_k
        )
        return results

    def delete_vectors(self, ids):
        self.client.delete_points(collection_name=self.collection_name, point_ids=ids)
