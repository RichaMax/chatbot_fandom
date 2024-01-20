from abc import ABC, abstractmethod


class Scraper(ABC):
    @abstractmethod
    def scrape(self) -> str:
        ...
