from fastapi import HTTPException
from demo_app.models.user import User
from demo_app.requests.user import UserCreateRequest
from demo_app.services.user_service import UserService
from sqlalchemy.orm import Session
from demo_app.repositories.user_repository import UserRepository
from demo_app.responses.user import UserResponse
from typing import Optional

class UserHandler:
    def __init__(self, service: UserService):
        self.service = service

    def handle_create_user(self, user_request: UserCreateRequest, db: Session) -> UserResponse:
        """ユーザー作成のハンドラ"""
        user = self.service.create_user(user_request, db)
        return UserResponse.from_orm(user)

    def handle_get_user(self, user_id: str, db: Session) -> Optional[UserResponse]:
        """ユーザー取得のハンドラ"""
        user = self.service.get_user(user_id, db)
        return UserResponse.from_orm(user)
