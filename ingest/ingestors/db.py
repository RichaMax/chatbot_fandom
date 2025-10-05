from pymongo import MongoClient
from clients.database.models import Page
from sqlalchemy import create_engine


class DBIngestor:
    def __init__(self, game: str):
        self.engine = create_engine("postgres://localhost:5432")

    def ingest_page(self, page: Page):
        pass
