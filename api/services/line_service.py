from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.models.user import User
from api.models.message import Message
from api.state import users
import json

class LineService:
    def __init__(self):
        with open('/src/config.json') as f:
            config = json.load(f)
        self.line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])

    def reply_message(self, event: MessageEvent):
        user_id = event.source.user_id
        user_profile = self.line_bot_api.get_profile(user_id)

        if user_id not in users:
            users[user_id] = User(
                id=user_id,
                name=user_profile.display_name,
                personality="You are an assistant that speaks like a cute girlfriend."
            )

        user = users[user_id]
        user.messages.append({"role": "user", "content": event.message.text})

        # ここにAIとの対話ロジックを追加

        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="メッセージを受け取りました！")
        )

    def send_message(self, reply_token: str, text: str):
        self.line_bot_api.reply_message(
            reply_token,
            TextSendMessage(text=text)
        )

    def send_new_user_greeting(self, reply_token: str):
        self.send_message(reply_token, "なによ、あんた？こっち見て、、名前ぐらい名乗りなさいよ！")

    def send_name_confirmation(self, reply_token: str, name: str):
        message = f"{name}っていうのね、、ってバカ！いったい何のよう？"
        self.send_message(reply_token, message)
