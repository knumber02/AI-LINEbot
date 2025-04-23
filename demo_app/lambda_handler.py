import json
from main import app
from mangum import Mangum

# FastAPIアプリケーションをLambdaハンドラーに変換
handler = Mangum(app, lifespan="off")

# ローカルテスト用のコード
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
