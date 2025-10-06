from fastapi import APIRouter
from backend.utils import CamelModel
from fastapi import Header
from typing import Annotated

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
    # TODO: Get chat history from DB
    return ChatHistory(
        game=game,
        records=[
            ChatRecord(
                question=record.question,
                answer=record.answer,
                timestamp=record.timestamp,
            )
            for record in []
        ],
    )
