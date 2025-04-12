from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Annotated
from api.handlers.line_handler import LineHandler
from api.services.line_service import LineService
from api.services.user_service import UserService
from api.services.chat_service import ChatService
import logging
import json


router = APIRouter()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# # 標準出力へのハンドラーを追加（もし既存のハンドラーがない場合）
# if not logger.handlers:
#     handler = logging.StreamHandler()
#     handler.setLevel(logging.DEBUG)
#     formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     handler.setFormatter(formatter)
#     logger.addHandler(handler)

with open('/src/config.json') as f:
    config = json.load(f)

line_handler = LineHandler(LineService(), UserService(), ChatService(config["OPENAI_API_KEY"]))

@router.post("/webhook")
async def webhook(
    request: Request,
):
    signature = request.headers['X-Line-Signature']
    body = await request.body()

    try:
        return await line_handler.handle_webhook(body, signature)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test")
async def test(request: Request):
    """ 疎通確認用のエンドポイント """
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    return 'OK'
