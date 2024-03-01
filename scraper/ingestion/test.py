import asyncio
from parser.main import parse_wiki
import hashlib
from openai import OpenAI
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key:str
    pinecone_api_key:str

settings = Settings()


client = OpenAI(
    api_key=settings.openai_api_key
)  # get API key from platform.openai.com

MODEL = "text-embedding-3-small"

result = asyncio.run(parse_wiki("valheim"))
for r in result:
    meta = {"title": r.page.title,
            "categories": r.page.categories,
            "url": r.link}
    print(meta)
    content = r.page.content
    print(content)
    page_embeddings = client.embeddings.create(
        model="text-embedding-3-small",
        input=content).data[0].embedding
    print(page_embeddings)
    print(hashlib.sha256(r.page.title.encode('utf-8')).hexdigest())
    break