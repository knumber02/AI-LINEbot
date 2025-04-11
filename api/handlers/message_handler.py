from fastapi import HTTPException
from api.models.message import Message
from api.models.user import User
from api.state import users
from api.services.chat_service import ChatService
import os
import json

with open('/src/config.json') as f:
    config = json.load(f)

class MessageHandler:
    def __init__(self):
        self.chat_service = ChatService(api_key=config["OPENAI_API_KEY"])

    def handle_create_message(self, message: Message) -> str:
        """メッセージ作成のハンドラ"""
        if message.user_id not in users:
            raise HTTPException(status_code=404, detail="User not found")

        user = users[message.user_id]
        response_content = self.chat_service.get_chat_response(user, message.content)

        return response_content

    def handle_get_messages(self, user_id: str) -> list:
        """メッセージ取得のハンドラ"""
        if user_id not in users:
            raise HTTPException(status_code=404, detail="User not found")
        return users[user_id].messages 
