from pydantic import BaseModel
from datetime import datetime
from demo_app.responses.base import TimestampMixin, ResponseBase
from demo_app.models.user import UserBase


class UserResponse(UserBase, TimestampMixin, ResponseBase):
    """ユーザーレスポンス用モデル"""
    id: int

    class Config:
        from_attributes = True
