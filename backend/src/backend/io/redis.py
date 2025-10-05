from backend.utils import CamelModel


class ChatRecord(CamelModel):
    timestamp: str
    question: str
    answer: str
