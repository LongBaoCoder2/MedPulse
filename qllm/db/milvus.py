from pymilvus import Collection, CollectionSchema, DataType, FieldSchema, connections

from qllm.core import VectorDBManager


class MilvusManager(VectorDBManager):
    def initialize(self, host="localhost", port=19530):
        connections.connect("default", host=host, port=port)
        self.collection_name = "example_collection"
        schema = CollectionSchema(
            fields=[
                FieldSchema(
                    name="id", dtype=DataType.INT64, is_primary=True, auto_id=False
                ),
                FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=512),
            ]
        )
        self.collection = Collection(name=self.collection_name, schema=schema)
        self.collection.load()

    def insert_vectors(self, vectors):
        ids = [v["id"] for v in vectors]
        vectors = [v["values"] for v in vectors]
        self.collection.insert([ids, vectors])

    def query_vectors(self, vector, top_k=5):
        self.collection.load()
        results = self.collection.search(
            data=[vector],
            anns_field="vector",
            param={"metric_type": "L2", "params": {"nprobe": 10}},
            limit=top_k,
        )
        return results

    def delete_vectors(self, ids):
        self.collection.delete(f"id in {ids}")
