from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from demo_app.models.message import Message

class IMessageRepository(ABC):
    @abstractmethod
    def create(self, user_id: int, character_id: int, content: str, role: str, db: Session) -> Message:
        pass

    @abstractmethod
    def get_user_messages(self, user_id: int, limit: int, db: Session) -> list[Message]:
        pass
