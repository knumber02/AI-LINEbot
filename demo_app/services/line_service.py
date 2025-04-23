from linebot import LineBotApi
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from demo_app.models.user import User
from demo_app.models.message import Message
from demo_app.config import get_config
from demo_app.services.user_service import UserService
from sqlalchemy.orm import Session

config = get_config()

class LineService:
    def __init__(self, user_service: UserService):
        self.line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])
        self.user_service = user_service

    def reply_message(self, event: MessageEvent, db: Session):
        line_user_id = event.source.user_id
        user_profile = self.line_bot_api.get_profile(line_user_id)
        user = self.user_service.get_or_create_user(line_user_id, db)

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
