from datetime import datetime
from typing import List, Optional
from sqlalchemy import TIMESTAMP, VARCHAR, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Character(Base):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        comment="キャラクターID"
    )
    user_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        comment="所有ユーザーID"
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="キャラクター名"
    )
    age: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="年齢"
    )
    tone: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="話し方"
    )
    ending: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="語尾"
    )
    voice: Mapped[str] = mapped_column(
        VARCHAR(255),
        nullable=False,
        comment="声の特徴"
    )
    language: Mapped[str] = mapped_column(
        VARCHAR(50),
        nullable=False,
        comment="使用言語"
    )
    personality: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="性格"
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
    user: Mapped["User"] = relationship("User", back_populates="characters")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="character")
