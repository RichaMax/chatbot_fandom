from fastapi import APIRouter
from pydantic import BaseModel
from .gpt import GPT
import sys

router = APIRouter()

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    question: str
    answer: str

@router.post("/ask")
async def ask(question: Question):
    client = GPT()
    answer = await client.answer(question.question)
    print(sys.version_info)
    return Answer(question=question.question, answer=answer)
