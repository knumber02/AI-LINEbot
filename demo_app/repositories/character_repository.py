from sqlalchemy.orm import Session
from demo_app.models.user import User
from demo_app.db import engine
from demo_app.requests.user import UserCreateRequest
from typing import Optional
from demo_app.repositories.interfaces.character_repository_interface import ICharacterRepository
from demo_app.models.character import Character
from demo_app.config import get_config

class CharacterRepository(ICharacterRepository):
    def create(self, character: Character, db: Session) -> Character:
        """キャラクターを作成する"""
        db.add(character)
        db.commit()
        db.refresh(character)
        return character

    def get_default_character(self, db: Session) -> Character:
        """デフォルトのキャラクターを取得する"""
        return db.query(Character).filter(Character.user_id == None).first()
