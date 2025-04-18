from fastapi import HTTPException
from sqlalchemy.orm import Session
from api.models.user import User
from api.requests.user import UserCreateRequest
from api.responses.user import UserResponse
from api.repositories.interfaces.user_repository_interface import IUserRepository
from typing import Optional

class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def get_or_create_user(self, line_user_id: str, db: Session) -> User:
        """ユーザーを取得または作成"""
        user = self.repository.get_by_line_id(line_user_id, db)
        if user is None:
            # 新規ユーザー作成
            user_data = UserCreateRequest(
                line_user_id=line_user_id,
                name=None
            )
            user = self.repository.create(user_data, db)
        return user

    def get_user(self, user_id: str, db: Session) -> Optional[User]:
        """ユーザーを取得"""
        int_user_id = int(user_id)
        user = self.repository.get_by_id(int_user_id, db)
        if user is None:
            return None
        return user

    def create_user(self, user_data: UserCreateRequest, db: Session) -> User:
        """ユーザーを作成"""
        return self.repository.create(user_data, db)

    def update_user(self, user: User, db: Session) -> User:
        """ユーザーを更新"""
        return self.repository.update(user, db)
