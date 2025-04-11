from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageBase(BaseModel):
    """
    メッセージの基本情報を表すモデルです
    """
    content: str = Field(
        ...,
        description="メッセージの内容"
    )

class MessageCreate(MessageBase):
    """
    メッセージ作成処理のリクエストボディ
    """
    id: str = Field(
        ...,
        description="メッセージID"
    )
    user_id: str = Field(
        ...,
        description="ユーザーID"
    )

    class Config:
        from_attributes = True
