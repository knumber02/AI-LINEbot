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

    def get_or_create_user(self, line_user_id: str, db: Session) -> UserResponse:
        """ユーザーを取得または作成"""
        user = self.repository.get_by_line_id(line_user_id, db)
        if user is None:
            # 新規ユーザー作成
            user_data = UserCreateRequest(
                line_user_id=line_user_id,
                name=None
            )
            user = self.repository.create(user_data, db)
        return UserResponse.from_orm(user)

    def get_user(self, user_id: str, db: Session) -> Optional[UserResponse]:
        """ユーザーを取得"""
        int_user_id = int(user_id)
        user = self.repository.get_by_id(int_user_id, db)
        if user is None:
            return None
        return UserResponse.from_orm(user)

    def create_user(self, user_data: UserCreateRequest, db: Session) -> UserResponse:
        """ユーザーを作成"""
        user = self.repository.create(user_data, db)
        return UserResponse.from_orm(user)

    def update_user(self, user: User, db: Session) -> UserResponse:
        """ユーザーを更新"""
        updated_user = self.repository.update(user, db)
        return UserResponse.from_orm(updated_user)

    def update_user_personality(self, user_id: str, personality: str, db: Session) -> UserResponse:
        """ユーザーの性格設定を更新"""
        int_user_id = int(user_id)
        user = self.repository.update_personality(int_user_id, personality, db)
        return UserResponse.from_orm(user)
