from pinecone import Pinecone
from typing import Any
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pinecone_api_key: str

class PineconeDB:
    def __init__(self) -> None:
        settings = Settings()
        self.pc = Pinecone(api_key=settings.pinecone_api_key)

    def get_documents(self, query_embedding: list[float],
                      index_name: str ,
                      top_k: int = 5,
                      include_metadata: bool = True,
                      **query_kwargs: Any):
        index = self.pc.Index(index_name)

        result = index.query(vector=query_embedding,
                                        top_k=top_k, include_metadata=include_metadata,
                                        **query_kwargs)
        
        return result['matches']