from abc import ABC, abstractmethod
from sqlalchemy.orm import Session

class Seeder(ABC):
    @abstractmethod
    def run(self, db: Session) -> None:
        pass
