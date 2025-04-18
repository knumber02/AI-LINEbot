from fastapi import FastAPI
from api.routes.line_routes import router as line_router
from api.routes.user_routes import router as user_router
import json
import openai
from pydantic import BaseModel
from config import load_config
app = FastAPI()

# ルーターの登録
app.include_router(line_router, prefix="/line", tags=["line"])
app.include_router(user_router, prefix="/users", tags=["users"])

# 設定ファイルの読み込み
config = load_config()
