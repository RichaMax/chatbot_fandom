from sqlalchemy import create_engine
# from models.db import User, Page, Chunk

class Database:
    def __init__(self):
        pass

    # ----- Pages -----

    def store_chunked_page(self, chunked_page):
        pass

    def get_chunk_content(self, chunk_id) -> str:
        return ""

    # ----- Chat -----

    def store_chat(self, user_id: int, question: str, answer: str):
        pass

    def get_chat_history(self, user_id: int) -> list[ChatRecord]:
        return []

    # ----- Users -----

    def is_user_password_hash_valid(self, username: str, password_hash: str) -> bool:
        return False

    def create_user(self, username: str, password_hash: str) -> User | None:
        pass
    
