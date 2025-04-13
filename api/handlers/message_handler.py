from fastapi import HTTPException
from api.models.message import Message
from api.requests.message import MessageCreate
from api.responses.message import MessageResponse
from api.services.chat_service import ChatService
from api.state import users
import json
from datetime import datetime
from config import get_config

config = get_config()

class MessageHandler:
    def __init__(self):
        self.chat_service = ChatService(api_key=config["OPENAI_API_KEY"])

    def handle_create_message(self, message_request: MessageCreate) -> MessageResponse:
        """メッセージ作成のハンドラ"""
        message = Message(
            id=message_request.id,
            user_id=message_request.user_id,
            content=message_request.content
        )
        if message.user_id not in users:
            raise HTTPException(status_code=404, detail="User not found")

        user = users[message.user_id]
        response_content = self.chat_service.get_chat_response(user, message.content)
        
        return MessageResponse(
            id=message.id,
            user_id=message.user_id,
            content=response_content,
            created_at=datetime.now()
        )

        return response_content

    def handle_get_messages(self, user_id: str) -> list:
        """ユーザーのメッセージ一覧取得のハンドラ"""
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        return users[user_id].messages
