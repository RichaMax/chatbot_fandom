from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass

from parser.temp import Page


@dataclass
class PageParsingError:
    link: str
    error_trace: str


@dataclass
class ParsingResult:
    pages: list[Page]
    errors: list[PageParsingError]


class Runner(ABC):
    @abstractmethod
    async def run(self) -> ParsingResult:
        ...
