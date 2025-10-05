from pydantic import BaseModel
from . import CamelModel


class ChatRecord(CamelModel):
    question: str
    answer: str
