from fastapi import APIRouter, Depends
from api.models.message import Message
from api.handlers.message_handler import MessageHandler
from typing import Annotated

router = APIRouter()

@router.post("/")
def create_message(message: Message, message_handler: Annotated[MessageHandler, Depends(MessageHandler)]):
    return message_handler.handle_create_message(message)

@router.get("/{user_id}")
def read_messages(user_id: str, message_handler: Annotated[MessageHandler, Depends(MessageHandler)]):
    return message_handler.handle_get_messages(user_id)
