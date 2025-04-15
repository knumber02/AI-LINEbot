from fastapi import HTTPException
from api.models.user import User
from api.requests.user import UserCreateRequest
from api.services.user_service import UserService
from sqlalchemy.orm import Session
from api.repositories.user_repository import UserRepository
from api.responses.user import UserResponse

class UserHandler:
    def __init__(self):
        self.user_service = UserService()

    def handle_create_user(self, user_request: UserCreateRequest, db: Session) -> UserResponse:
        """ユーザー作成のハンドラ"""
        return self.user_service.create_user(user_request, db)

    def handle_get_user(self, user_id: str, db: Session) -> UserResponse:
        """ユーザー取得のハンドラ"""
        return self.user_service.get_user(user_id, db)

    def handle_update_personality(self, user_id: str, personality: str, db: Session) -> UserResponse:
        """ユーザーの性格設定更新のハンドラ"""
        return self.user_service.update_user_personality(user_id, personality, db)
