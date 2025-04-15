from pydantic import BaseModel, Field
from typing import Optional
from api.requests.base import RequestBase
from api.models.user import UserBase

class UserCreateRequest(UserBase, RequestBase):
    """
    ユーザー作成処理のリクエストボディです
    """
    pass

class UserPersonalityUpdateRequest(RequestBase):
    """
    ユーザーの性格設定更新処理のリクエストボディです
    """
    personality: str = Field(
        ...,
        description="新しい性格設定"
    ) 
