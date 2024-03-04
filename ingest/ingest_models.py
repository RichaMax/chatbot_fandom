from pydantic import BaseModel
from pydantic.dataclasses import dataclass

@dataclass
class Ref:
    # we will have issues with redirects there
    link: str
    text: str


@dataclass
class Text:
    content: str


@dataclass
class Line:
    content: list[Text | Ref]


@dataclass
class Paragraph:
    lines: list[Line]


@dataclass
class TableRow:
    cells: list[Text | Ref]


@dataclass
class Table:
    rows: list[TableRow]


PageContent = list[Paragraph | Table]

class PageMetadata(BaseModel):
    title: str
    url: str
    categories: list[str]

class ScrappedPage(BaseModel):
    title: str
    categories: list[str]
    content: PageContent
    str_content: str

class Page(BaseModel):
    metadata: PageMetadata
    content: PageContent
    str_content: str

class Chunk(BaseModel):
    id: str
    content: str

class ChunkedPage(BaseModel):
    chunks: list[Chunk]
    metadata: PageMetadata


class EmbeddedChunk(Chunk):
    embedding: list[float]

class EmbeddedPage(BaseModel):
    metadata: PageMetadata
    chunks: list[EmbeddedChunk]