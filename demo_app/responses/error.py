from pydantic import BaseModel, Field

class ErrorResponse(BaseModel):
    """
    エラーレスポンスのモデルです
    """
    detail: str = Field(
        ...,
        description="エラーの詳細メッセージ"
    ) 
