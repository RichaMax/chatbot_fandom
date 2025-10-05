from fastapi import APIRouter
from backend.utils import CamelModel
import redis.asyncio as redis
from fastapi import Header
from typing import Annotated
from backend.io.redis import ChatRecord as RedisChatRecord

router = APIRouter()


class ChatRecord(CamelModel):
    question: str
    answer: str


class ChatHistory(CamelModel):
    game: str
    records: list[ChatRecord]


@router.get("/games/{game}/history")
async def get_history(game: str, session_id: Annotated[str, Header()]):
    print(f"Sesssion ID: {session_id}")
    client: redis.Redis = redis.Redis(host="cache")
    records = await client.lrange(f"user:{session_id}:game:{game}", -20, -1)
    records = [RedisChatRecord.parse_raw(record) for record in records]
    return ChatHistory(
        game=game,
        records=[
            ChatRecord(
                question=record.question,
                answer=record.answer,
                timestamp=record.timestamp,
            )
            for record in records
        ],
    )
