from fastapi import APIRouter
from pydantic import BaseModel
from .gpt import GPT

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
    return Answer(question=question.question, answer=answer)
