from sqlalchemy.orm import Session
from api.models.character import Character
from config import get_config
from .interface import Seeder

class CharacterSeeder(Seeder):
    def run(self, db: Session) -> None:
        config = get_config()
        default_character = config['default_character']

        character = Character(
            name=default_character["name"],
            age=default_character["age"],
            tone=default_character["tone"],
            ending=default_character["ending"],
            voice=default_character["voice"],
            language=default_character["language"],
            personality=default_character["personality"]
        )
        db.add(character)
