from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Annotated
from sqlalchemy.orm import Session
from ..db import get_db
from ..handlers.line_handler import LineHandler
from ..services.line_service import LineService
from ..services.user_service import UserService
from ..services.chat_service import ChatService
from ..repositories.user_repository import UserRepository
from ..repositories.message_repository import MessageRepository
from ..models.character import Character
import json
from ..repositories.interfaces.message_repository_interface import IMessageRepository
from ..repositories.interfaces.character_repository_interface import ICharacterRepository
from ..repositories.character_repository import CharacterRepository
from api.dependencies import get_line_handler


router = APIRouter()


@router.post("/webhook")
async def line_webhook(
    request: Request,
    line_handler: LineHandler = Depends(get_line_handler),
):
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    try:
        return line_handler.handle_webhook(body, signature)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test(request: Request):
    """ 疎通確認用のエンドポイント """
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    return 'OK'
