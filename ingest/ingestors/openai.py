from openai import AsyncOpenAI
from pydantic_settings import BaseSettings

MODEL = "text-embedding-3-small"

class Settings(BaseSettings):
    openai_api_key:str

class Embedder:
    def __init__(self):
        settings = Settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
    
    async def embed(self, content: str) -> list[float]:
        result = await self.client.embeddings.create(
            model=MODEL,
            input=content
        )

        return result.data[0].embedding
