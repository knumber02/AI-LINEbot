from pydantic import BaseModel
from datetime import datetime

class ResponseBase(BaseModel):
    """全レスポンスの基底クラス"""
    class Config:
        from_attributes = True

class TimestampMixin(BaseModel):
    """タイムスタンプを持つレスポンス用Mixin"""
    created_at: datetime
    updated_at: datetime
