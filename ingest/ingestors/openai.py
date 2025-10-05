from openai import AsyncOpenAI
from pydantic_settings import BaseSettings
from utils import cut_batches
import itertools
import asyncio

MODEL = "text-embedding-3-small"

class Settings(BaseSettings):
    openai_api_key: str


class Embedder:
    def __init__(self):
        settings = Settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def embed(self, content: list[str]) -> list[list[float]]:
        batches = cut_batches(content, batch_size=50)

        return [
            data.embedding
            for result in await asyncio.gather(
                    *[
                        self.client.embeddings.create(
                            model=MODEL,
                            input=batch,
                        )
                        for batch in batches
                    ]
                )
            for data in result.data
        ]
