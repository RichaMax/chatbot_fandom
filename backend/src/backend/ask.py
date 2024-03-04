from .pinecone_connector import PineconeDB
from .mongo import Mongo
from fastapi import APIRouter
from pydantic import BaseModel
from .gpt import GPT
import sys
import logging 

logger = logging.getLogger()

router = APIRouter()

class Question(BaseModel):
    question: str
    game: str

class Answer(BaseModel):
    question: str
    answer: str

@router.post("/ask")
async def ask(question: Question):
    client = GPT()
    pc = PineconeDB()
    mongo = Mongo()

    embedding = await client.embed(question.question)

    docs = pc.get_documents(embedding, question.game, top_k=3)

    print(f"documents : {docs}")

    best_match = docs[0]

    chunk = mongo.get_chunk(question.game, best_match["id"])

    

    # answer = await client.answer(question.question)
    return Answer(question=question.question, answer="lol")
