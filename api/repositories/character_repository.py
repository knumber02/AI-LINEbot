from sqlalchemy.orm import Session
from api.models.user import User
from api.db import engine
from api.requests.user import UserCreateRequest
from typing import Optional
from .interfaces.character_repository_interface import ICharacterRepository
from api.models.character import Character
from config import get_config

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
