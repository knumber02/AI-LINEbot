from sqlalchemy.orm import Session
from demo_app.models.user import User
from demo_app.db import engine
from demo_app.requests.user import UserCreateRequest
from typing import Optional
from demo_app.repositories.interfaces.user_repository_interface import IUserRepository

class UserRepository(IUserRepository):
    def get_by_id(self, user_id: int, db: Session) -> Optional[User]:
        """ユーザーをIDで取得する"""
        return db.query(User).filter(User.id == user_id).first()

    def get_by_line_id(self, line_user_id: str, db: Session) -> Optional[User]:
        return db.query(User).filter(User.line_user_id == line_user_id).first()

    def create(self, user_data: UserCreateRequest, db: Session) -> User:
        """ユーザーを作成する"""
        user = User(**user_data.dict(exclude_unset=True))
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, user: User, db: Session) -> User:
        """ユーザーを更新する"""
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
