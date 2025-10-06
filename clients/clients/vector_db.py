import uuid
from qdrant_client.models import VectorParams, Distance, PointStruct
from qdrant_client.async_qdrant_client import AsyncQdrantClient

VECTOR_SIZE = 1028

class VectorDatabase:
    def __init__(self) -> None:
        self.client = AsyncQdrantClient(url="http://localhost:6333")

    async def get_or_create_collection(self, collection: str):
        if not await self.client.collection_exists(collection):
            await self.client.create_collection(
                collection_name=collection,
                vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE),
            )

    async def save_embeddings(self, collection: str, ids: list[uuid.UUID], vectors: list[list[float]]):
        await self.client.upsert(
            collection_name=collection,
            points=[
                PointStruct(
                    id=id,
                    vector=vector,
                )
                for id, vector in zip(ids, vectors)
            ]
        )
    
    async def get_top_neighbours(self, n: int, embedding: list[float]) -> uuid.UUID:
        return uuid.uuid4()
