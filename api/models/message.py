from datetime import datetime
from typing import Optional, List
from sqlalchemy import TIMESTAMP, VARCHAR, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.declarative import declarative_base
from .base import Base

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="メッセージID"
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        comment="ユーザーID"
    )
    character_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("characters.id"),
        nullable=False,
        comment="キャラクターID"
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="メッセージ内容"
    )
    role: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        comment="メッセージの役割(user/assistant)"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=datetime.now,
        comment="作成日時"
    )

    # リレーションシップを定義
    user: Mapped["User"] = relationship("User", back_populates="messages")
    character: Mapped["Character"] = relationship("Character", back_populates="messages")
