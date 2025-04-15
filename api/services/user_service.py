from fastapi import HTTPException
from api.models.user import User
from api.requests.user import UserCreateRequest
from api.state import users
from typing import Optional
from api.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from api.responses.user import UserResponse

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def get_or_create_user(self, user_id: str) -> User:
        """ユーザーを取得または作成"""
        if user_id not in users:
            users[user_id] = User(id=user_id, name=None)
        return users[user_id]

    def get_user(self, user_id: str, db: Session) -> Optional[UserResponse]:
        """ユーザーを取得します"""
        int_user_id = int(user_id)
        user = self.user_repository.get_by_id(int_user_id, db)
        if user is None:
            return None
        return UserResponse.from_orm(user)

    def create_user(self, user_data: UserCreateRequest, db: Session) -> UserResponse:
        """ユーザーを作成します"""
        user = self.user_repository.create(user_data, db)

        return UserResponse.from_orm(user)

    def update_user(self, user: User) -> User:
        """ユーザーを更新します"""
        users[user.id] = user
        return user

    def update_user_personality(self, user_id: str, personality: str, db: Session) -> UserResponse:
        """ユーザーの性格設定を更新します"""
        int_user_id = int(user_id)
        user = self.user_repository.update_personality(int_user_id, personality, db)
        return UserResponse.from_orm(user)
