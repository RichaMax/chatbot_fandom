from pydantic.dataclasses import dataclass


@dataclass
class Ref:
    # we will have issues with redirects there
    link: str


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


@dataclass
class Page:
    link: str
    categories: list[str]
    title: str
    content: PageContent
