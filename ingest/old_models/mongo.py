from pydantic import BaseModel
from enum import StrEnum


class Collections(StrEnum):
    PAGES = "pages"


class Chunk(BaseModel):
    id: str
    content: str


class Page(BaseModel):
    title: str
    url: str
    categories: list[str]
    chunks: list[Chunk]
