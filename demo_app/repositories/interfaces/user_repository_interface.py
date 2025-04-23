from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from demo_app.models.user import User
from demo_app.requests.user import UserCreateRequest

class IUserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int, db: Session) -> Optional[User]:
        pass

    @abstractmethod
    def get_by_line_id(self, line_user_id: str, db: Session) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user_data: UserCreateRequest, db: Session) -> User:
        pass

    @abstractmethod
    def update(self, user: User, db: Session) -> User:
        pass
