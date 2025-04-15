from datetime import datetime
from typing import List
from sqlalchemy import TIMESTAMP, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

# SQLAlchemy Model (ORM)
class User(Base):
    """データベースのユーザーテーブルを表現するORMモデル"""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="ユーザーID"
    )
    line_user_id: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
        nullable=False,
        comment="LINE User ID"
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="ユーザー名"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now,
        comment="作成日時"
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新日時"
    )

    # リレーションシップを定義
    characters: Mapped[List["Character"]] = relationship("Character", back_populates="user")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")


# Pydantic Models
class UserBase(BaseModel):
    """ユーザーの基本情報を表すPydanticモデル"""
    line_user_id: str = Field(..., description="LINE User ID")
    name: Optional[str] = Field(None, description="ユーザー名")

    def to_dict(self) -> Dict[str, Any]:
        """ORMモデルに変換可能な辞書を返す"""
        return self.dict(exclude_unset=True)
