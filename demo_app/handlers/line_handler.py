from fastapi import Depends, HTTPException
from typing import Annotated
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from demo_app.services.line_service import LineService
from demo_app.services.user_service import UserService
from demo_app.services.chat_service import ChatService
from demo_app.models.user import User
import json
from demo_app.config import get_config
from sqlalchemy.orm import Session

config = get_config()

class LineHandler:
    def __init__(
        self,
        line_service: LineService,
        user_service: UserService,
        chat_service: ChatService,
        db: Session
    ):
        self.line_service = line_service
        self.user_service = user_service
        self.chat_service = chat_service
        self.db = db
        self.handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])

        # メッセージハンドラーの登録
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            self._process_message(event, self.db)

    def handle_webhook(self, request_body: bytes, signature: str) -> str:
        """Webhookのハンドラ"""
        try:
            self.handler.handle(request_body.decode(), signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        return "OK"

    def _process_message(self, event: MessageEvent, db: Session):
        """メッセージ処理のメインロジック"""
        line_user_id = event.source.user_id
        text = event.message.text

        user = self.user_service.get_or_create_user(line_user_id, db)

        # 新規ユーザーの場合
        if user.name is None:
            self._handle_new_user(event, user, text, db)
            return

        # チャット応答の生成と送信
        response = self.chat_service.generate_response(user, text, db)
        self.line_service.send_message(event.reply_token, response)

    def _handle_new_user(self, event: MessageEvent, user: User, text: str, db: Session):
        """新規ユーザーの処理"""
        if user.name is None and not user.greeted:
            # 最初のメッセージ（名前を尋ねる）
            user.greeted = True
            user = self.user_service.update_user(user, db)
            self.line_service.send_new_user_greeting(event.reply_token)
            return

        if user.name is None and user.greeted:
            # 2回目のメッセージ（名前を設定）
            user.name = text
            self.user_service.update_user(user, db)
            self.line_service.send_name_confirmation(event.reply_token, text)
            return
