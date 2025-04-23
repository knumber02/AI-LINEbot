from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from demo_app.models.character import Character

class ICharacterRepository(ABC):
    @abstractmethod
    def create(self, character: Character, db: Session) -> Character:
        pass

    @abstractmethod
    def get_default_character(self, db: Session) -> Character:
        pass
