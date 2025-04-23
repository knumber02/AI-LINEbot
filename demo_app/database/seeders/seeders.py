from sqlalchemy.orm import Session
from .interface import Seeder
from .character_seeder import CharacterSeeder

class SeederRunner:
    def __init__(self) -> None:
        self._seeders: list[Seeder] = [
            CharacterSeeder(),
        ]

    def run(self, db: Session) -> None:
        for seeder in self._seeders:
            seeder.run(db)
            db.flush()
