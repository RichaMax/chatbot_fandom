from backend.io.pinecone_connector import PineconeDB
from backend.io.mongo import Mongo
from fastapi import APIRouter
from pydantic import BaseModel
from backend.io.gpt import GPT
import sys
import logging
import redis.asyncio as redis
import asyncio
from backend.io.redis import ChatRecord as RedisChatRecord
from fastapi import Header
from typing import Annotated
import time

logger = logging.getLogger()

router = APIRouter()


class Question(BaseModel):
    question: str
    game: str


class Answer(BaseModel):
    question: str
    answer: str


@router.post("/ask")
async def ask(question: Question, session_id: Annotated[str, Header()]):
    print(f"Sesssion ID: {session_id}")
    client = GPT()
    redis_client: redis.Redis = redis.Redis(host="cache")
    pc = PineconeDB()
    mongo = Mongo()

    embedding = await client.embed(question.question)

    docs = pc.get_documents(embedding, question.game, top_k=5)

    info = ""

    prompt = f"You are a helpful assistant for the game {question.game}.\nYou know this:\n{info}\nIf the question has nothing to do with Valheim, inform the user and do not answer\nQuestion: {question.question}"
    answer = await client.answer(prompt, question.question)
    record = RedisChatRecord(
        question=question.question, answer=answer, timestamp=str(time.time())
    )
    await redis_client.rpush(
        f"user:{session_id}:game:{question.game}", record.model_dump_json()
    )
    return Answer(question=question.question, answer=answer)
