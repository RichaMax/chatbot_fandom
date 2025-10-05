from pymongo import MongoClient
from models.mongo import Page, Collections


class MongoIngestor:
    def __init__(self, game: str):
        self.client = MongoClient()
        self.database = self.client[game]

    def ingest_page(self, page: Page):
        self.database[Collections.PAGES].insert_one(page.model_dump())
