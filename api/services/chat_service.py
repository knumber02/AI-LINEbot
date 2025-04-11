import openai
import random
from api.models.user import User
from api.state import characters
from typing import List, Dict

class ChatService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.chat_model = "gpt-3.5-turbo"
        self.inappropriate_words = ['inappropriate', 'offensive']
        self.character = characters["default"]  # デフォルトキャラクターを取得

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

    def generate_response(self, user: User, text: str) -> str:
        # ユーザーの名前を追加
        text_with_name = f"{user.name}さん、{text}"
        user.messages.append({"role": "user", "content": text_with_name})

        # 会話履歴の準備
        conversation_history = user.messages[-10:]
        conversation_history.insert(0, {
            "role": "system",
            "content": f"your role is to embody the following character: Age: {self.character.age}\nName: {self.character.name}\nTone: {self.character.tone}\nEnding: {self.character.ending}\nVoice: {self.character.voice}\nLanguage: {self.character.language}\nPersonality: {self.character.personality}"
        })

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

        user.messages.append({"role": "assistant", "content": response_content})
        return response_content
