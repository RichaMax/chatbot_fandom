from pymongo import MongoClient


class Mongo:
    def __init__(self):
        self.client = MongoClient("mongodb")

    def get_chunk(self, game: str, chunk_id: str):
        result = self.client[game]["pages"].find_one({"chunks.id": chunk_id}, {"chunks.$": 1})
        print(result)