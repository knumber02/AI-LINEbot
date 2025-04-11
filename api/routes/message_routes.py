from fastapi import APIRouter
from api.models.message import Message
from api.handlers.message_handler import MessageHandler

router = APIRouter()
message_handler = MessageHandler()

@router.post("/messages/")
def create_message(message: Message):
    return message_handler.handle_create_message(message)

@router.get("/messages/{user_id}")
def read_messages(user_id: str):
    return message_handler.handle_get_messages(user_id) 
