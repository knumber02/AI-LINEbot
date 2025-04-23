import openai
import random
from demo_app.models.user import User
from typing import List, Dict, Optional
from demo_app.repositories.interfaces.message_repository_interface import IMessageRepository
from demo_app.models.character import Character
from sqlalchemy.orm import Session
from demo_app.services.character_service import CharacterService

class ChatService:
    def __init__(self, api_key: str, message_repository: IMessageRepository, character_service: CharacterService):
        openai.api_key = api_key
        self.chat_model = "gpt-3.5-turbo"
        self.inappropriate_words = ['inappropriate', 'offensive']
        self.message_repository = message_repository
        self._character: Optional[Character] = None
        self.character_service = character_service

    def get_chat_response(self, user: User, message: str) -> str:
        """チャットレスポンスを取得"""
        if not openai.api_key:
            return "OpenAI API key is not set."

        # メッセージを履歴に追加
        user.messages.append({"role": "user", "content": message})

        try:
            # 会話履歴を準備
            conversation_history = user.messages[-10:]  # 最新10件に制限
            conversation_history.insert(0, {"role": "system", "content": user.personality})

            # OpenAI APIを呼び出し
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=conversation_history
            )
            response_content = response['choices'][0]['message']['content']

            # 不適切なコンテンツをフィルタリング
            if any(word in response_content for word in self.inappropriate_words):
                response_content = "I'm sorry, but I can't assist with that."

            # アシスタントのレスポンスを履歴に追加
            user.messages.append({"role": "assistant", "content": response_content})

            return response_content

        except Exception as e:
            error_message = f"Error: {str(e)}"
            user.messages.append({"role": "assistant", "content": error_message})
            return error_message

    def generate_response(self, user: User, text: str, db: Session) -> str:
        # ユーザーメッセージを保存
        character = self._get_character(db)
        self.message_repository.create(
            user_id=user.id,
            character_id=character.id,
            content=text,
            role="user",
            db=db
        )

        # 最近のメッセージを取得
        recent_messages = self.message_repository.get_user_messages(user.id, 10, db)
        
        # 会話履歴の準備
        conversation_history = [
            {
                "role": msg.role,
                "content": msg.content
            } for msg in recent_messages
        ]

        # システムメッセージを追加
        system_message = {
            "role": "system",
            "content": f"your role is to embody the following character: Age: {character.age}\nName: {character.name}\nTone: {character.tone}\nEnding: {character.ending}\nVoice: {character.voice}\nLanguage: {character.language}\nPersonality: {character.personality}"
        }
        conversation_history.insert(0, system_message)

        try:
            response = openai.ChatCompletion.create(
                model=self.chat_model,
                messages=conversation_history
            )
            response_content = response['choices'][0]['message']['content']

            # 不適切なコンテンツのフィルタリング
            if any(word in response_content for word in self.inappropriate_words):
                response_content = "I'm sorry, but I can't assist with that."

            # エモジの追加
            emoji = random.choice(['❤️', '...', '♪'])
            response_content = f"{response_content} {emoji}"

        except Exception as e:
            response_content = "ごめんなさい、今ちょっと眠いの... もう少し待っててくれる？"
            print(f'Error occurred: {str(e)}')

        self.message_repository.create(
            user_id=user.id,
            character_id=character.id,
            content=response_content,
            role="assistant",
            db=db
        )
        return response_content

    def _get_character(self, db: Session) -> Character:
        if self._character is None:
            self._character = self.character_service.get_default_character(db)
        return self._character
