import asyncio
import time

from openai import AsyncOpenAI
from pinecone import Pinecone, ServerlessSpec, Vector
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from models.pinecone import ChunkMetadata
from ingest.ingest_models import EmbeddedPage
from ingest.utils import cut_batches
from rich.progress import track


class Settings(BaseSettings):
    pinecone_api_key: str


PINECONE_SPEC = ServerlessSpec(cloud="aws", region="us-west-2")


class PineconeIngestor:
    def __init__(self, game: str):
        settings = Settings()
        pinecone_client = Pinecone(api_key=settings.pinecone_api_key)

        if game not in pinecone_client.list_indexes().names():
            # if does not exist, create index
            pinecone_client.create_index(
                game,
                dimension=1536,  # dimensionality of text-embed-3-small
                metric="dotproduct",
                spec=PINECONE_SPEC,
            )
            # wait for index to be initialized
            while not pinecone_client.describe_index(game).status["ready"]:
                time.sleep(1)

        self.index = pinecone_client.Index(game)

    def ingest_pages(self, pages: list[EmbeddedPage]):
        vectors = [
            Vector(
                id=chunk.id,
                values=chunk.embedding,
                metadata=ChunkMetadata(
                    title=page.metadata.title,
                    categories=page.metadata.categories,
                    url=page.metadata.url,
                    chunk_order=i,
                ).model_dump(),
            )
            for page in pages
            for i, chunk in enumerate(page.chunks)
        ]

        batches = cut_batches(vectors, batch_size=200)

        for batch in track(batches, description="Saving vectors ..."):
            self.index.upsert(batch)

    def ingest_page(self, page: EmbeddedPage):
        metadata = ChunkMetadata(
            title=page.metadata.title,
            categories=page.metadata.categories,
            url=page.metadata.url,
            chunk_order=0,
        )

        self.index.upsert(
            [
                Vector(
                    id=chunk.id, values=chunk.embedding, metadata=metadata.model_dump()
                )
                for chunk in page.chunks
            ]
        )
