from fastapi import APIRouter, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.services.line_service import LineService
import os
import json

router = APIRouter()

with open('/src/config.json') as f:
    config = json.load(f)

line_bot_api = LineBotApi(config["LINE_CHANNEL_ACCESS_TOKEN"])
handler = WebhookHandler(config["LINE_CHANNEL_SECRET"])
line_service = LineService(line_bot_api, handler)

@router.post("/webhook")
async def webhook(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()

    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_service.handle_message(event) 
