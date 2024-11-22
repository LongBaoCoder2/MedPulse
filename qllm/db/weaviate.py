import weaviate

from qllm.core import VectorDBManager


class WeaviateManager(VectorDBManager):
    def initialize(self, host="http://localhost:8080"):
        self.client = weaviate.Client(host)
        self.class_name = "ExampleVector"
        if not self.client.schema.contains({"class": self.class_name}):
            self.client.schema.create_class(
                {"class": self.class_name, "vectorizer": "none"}
            )

    def insert_vectors(self, vectors):
        for v in vectors:
            self.client.data_object.create(
                data_object=v["metadata"],
                class_name=self.class_name,
                vector=v["values"],
            )

    def query_vectors(self, vector, top_k=5):
        results = (
            self.client.query.get(self.class_name)
            .with_near_vector({"vector": vector})
            .with_limit(top_k)
            .do()
        )
        return results

    def delete_vectors(self, ids):
        for id_ in ids:
            self.client.data_object.delete(uuid=id_)
