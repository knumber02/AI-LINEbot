import openai
from api.models.user import User
from typing import List, Dict

class ChatService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.chat_model = "gpt-3.5-turbo"
        self.inappropriate_words = ['inappropriate', 'offensive']

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
