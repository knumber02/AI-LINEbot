from pydantic import BaseModel
from datetime import datetime
from api.responses.base import TimestampMixin, ResponseBase
from api.models.user import UserBase


class UserResponse(UserBase, TimestampMixin, ResponseBase):
    """ユーザーレスポンス用モデル"""
    id: int

    class Config:
        from_attributes = True
