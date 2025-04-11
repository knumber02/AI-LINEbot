from pydantic import BaseModel, Field
from datetime import datetime

class MessageResponse(BaseModel):
    """
    メッセージのレスポンスモデルです
    """
    id: str = Field(
        ...,
        description="メッセージID"
    )
    user_id: str = Field(
        ...,
        description="ユーザーID"
    )
    content: str = Field(
        ...,
        description="メッセージの内容"
    )
    created_at: datetime = Field(
        ...,
        description="作成日時"
    )

    class Config:
        from_attributes = True
