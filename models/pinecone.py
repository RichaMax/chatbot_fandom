from pydantic import BaseModel


class ChunkMetadata(BaseModel):
    title: str
    categories: list[str]
    url: str
    chunk_order: int
