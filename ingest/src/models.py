from pydantic import BaseModel, Field
from typing import Annotated, Any, Literal


class Ref(BaseModel):
    # we will have issues with redirects there
    link: str
    text: str
    type: Literal["ref"] = "ref"


class Header(BaseModel):
    content: str
    level: int
    type: Literal["header"] = "header"


class Text(BaseModel):
    content: str
    type: Literal["text"] = "text"


# @dataclass
# class Line:
#     line_content: list[Text | Ref]


# @dataclass
# class Paragraph:
#     lines: list[Line]


class List(BaseModel):
    elements: list[list[Text | Ref]]
    type: Literal["list"] = "list"


class TableRow(BaseModel):
    cells: list[list[Any]]
    type: Literal["table_row"] = "table_row"


class Table(BaseModel):
    type: Literal["table"] = "table"
    rows: list[TableRow]


PageElement = Annotated[
    Header | Text | Ref | List | Table, Field(..., discriminator="type")
]
PageContent = list[PageElement]


class PageMetadata(BaseModel):
    title: str
    url: str
    checksum: str
    categories: list[str]


class ScrappedPage(BaseModel):
    title: str
    categories: list[str]
    content: PageContent


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
