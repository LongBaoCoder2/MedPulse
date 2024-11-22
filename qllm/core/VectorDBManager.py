from abc import ABC, abstractmethod


class VectorDBManager(ABC):
    @abstractmethod
    def initialize(self, **kwargs):
        pass

    @abstractmethod
    def insert_vectors(self, vectors):
        pass

    @abstractmethod
    def query_vectors(self, vector, top_k=5):
        pass

    @abstractmethod
    def delete_vectors(self, ids):
        pass
