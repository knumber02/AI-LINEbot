from fastapi import FastAPI
from api.routes.line_routes import router as line_router
from api.routes.user_routes import router as user_router
from api.routes.message_routes import router as message_router
import json
import openai
from pydantic import BaseModel
from api.state import User, users
from middleware import create_middleware

app = FastAPI()

# ルーターの登録
app.include_router(line_router, prefix="/line", tags=["line"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(message_router, prefix="/messages", tags=["messages"])

# 設定ファイルの読み込み
with open('/src/config.json') as f:
    data = json.load(f)

# ミドルウェアの設定
app.middleware("http")(create_middleware())

# OpenAI APIキーの設定
openai.api_key = data['OPENAI_API_KEY']
