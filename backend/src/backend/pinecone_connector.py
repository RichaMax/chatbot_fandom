from pinecone import Pinecone
from typing import Any

class PineconeDB:
    def __init__(self, api_key: str, index_name: str | None = None) -> None:
        self.pc = Pinecone(api_key=api_key)
        if index_name:
            self.set_index(index_name)

    def set_index(self, index_name: str):
        self.index = self.pc.Index(index_name)

    def get_documents(self, query_embedding: list[float],
                      index_name: str | None = None,
                      top_k: int = 5,
                      include_metadata: bool = True,
                      **query_kwargs: Any):
        if index_name:
            self.set_index(index_name)
        if not self.index:
            raise AttributeError("PineconeDB attribut 'index' is not defined")

        matched_docs = self.index.query(vector=query_embedding,
                                        top_k=top_k, include_metadata=include_metadata,
                                        **query_kwargs)