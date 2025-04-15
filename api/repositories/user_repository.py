from sqlalchemy.orm import Session
from api.models.user import User
from api.database import engine
from api.requests.user import UserCreateRequest
from typing import Optional
class UserRepository:
    def create(self, user_data: UserCreateRequest, db: Session) -> User:
        """ユーザーを作成する"""
        user = User(**user_data.to_dict())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_by_id(self, user_id: int, db: Session) -> Optional[User]:
        """ユーザーをIDで取得する"""
        return db.query(User).filter(User.id == user_id).first()

    def update_personality(self, user_id: int, personality: str, db: Session) -> User:
        """ユーザーの性格を更新する"""
        user = db.query(User).filter(User.id == user_id).first()
        user.personality = personality
        db.commit()
        db.refresh(user)
        return user
