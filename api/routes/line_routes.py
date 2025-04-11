from fastapi import APIRouter, Request, HTTPException, Depends
from typing import Annotated
from api.handlers.line_handler import LineHandler

router = APIRouter()

@router.post("/webhook")
async def webhook(
    request: Request,
    line_handler: Annotated[LineHandler, Depends(LineHandler)]
):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    return await line_handler.handle_webhook(body, signature)
