from fastapi import Depends, HTTPException
from typing import Annotated
from linebot import WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from api.services.line_service import LineService
from api.services.user_service import UserService
from api.services.chat_service import ChatService
from api.models.user import User
import json

class LineHandler:
    def __init__(
        self,
        line_service: Annotated[LineService, Depends(LineService)],
        user_service: Annotated[UserService, Depends(UserService)],
        chat_service: Annotated[ChatService, Depends(ChatService)]
    ):
        with open('/src/config.json') as f:
            config = json.load(f)

        self.handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])
        self.line_service = line_service
        self.user_service = user_service
        self.chat_service = chat_service

        # メッセージハンドラーの登録
        @self.handler.add(MessageEvent, message=TextMessage)
        def handle_message(event):
            self._process_message(event)

    async def handle_webhook(self, request_body: bytes, signature: str) -> str:
        try:
            self.handler.handle(request_body.decode(), signature)
        except InvalidSignatureError:
            raise HTTPException(status_code=400, detail="Invalid signature")
        return "OK"

    def _process_message(self, event: MessageEvent):
        """メッセージ処理のメインロジック"""
        user_id = event.source.user_id
        text = event.message.text

        # ユーザー取得または作成
        user = self.user_service.get_or_create_user(user_id)

        # 新規ユーザーの場合
        if user.name is None:
            self._handle_new_user(event, user, text)
            return

        # チャット応答の生成と送信
        response = self.chat_service.generate_response(user, text)
        self.line_service.send_message(event.reply_token, response)

    def _handle_new_user(self, event: MessageEvent, user: User, text: str):
        """新規ユーザーの処理"""
        # 最初のメッセージ（名前を尋ねる）
        if user.name is None and user.greeted == False:
            user.greeted = True  # 挨拶済みフラグを設定
            self.user_service.update_user(user)
            self.line_service.send_new_user_greeting(event.reply_token)
            return
        
        # 2回目のメッセージ（名前を設定）
        if user.name is None and user.greeted == True:
            user.name = text  # 2回目のメッセージを名前として設定
            self.user_service.update_user(user)
            self.line_service.send_name_confirmation(event.reply_token, text)
            return
