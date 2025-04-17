from sqlalchemy.orm import Session
from api.models.character import Character
from api.repositories.character_repository import ICharacterRepository

class CharacterService:
    def __init__(self, character_repository: ICharacterRepository):
        self.character_repository = character_repository

    def get_default_character(self, db: Session) -> Character:
        character = self.character_repository.get_default_character(db)
        if character is None:
            raise ValueError("Default character not found")
        return character 
