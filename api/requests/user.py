from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    """
    ユーザーの基本情報を表すモデルです
    """
    name: str = Field(
        default=None,
        description="ユーザーの名前"
    )
    personality: Optional[str] = Field(
        default=None,
        description="ユーザーの性格設定"
    )

class UserCreateRequest(UserBase):
    """
    ユーザー作成処理のリクエストボディです
    """
    id: str = Field(
        ...,
        description="ユーザーID"
    )

class UserPersonalityUpdateRequest(BaseModel):
    """
    ユーザーの性格設定更新処理のリクエストボディです
    """
    personality: str = Field(
        ...,
        description="新しい性格設定"
    ) 
