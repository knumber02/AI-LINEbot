from fastapi import HTTPException
from api.models.user import User
from api.requests.user import UserCreateRequest
from api.services.user_service import UserService

class UserHandler:
    def __init__(self):
        self.user_service = UserService()

    def handle_create_user(self, user_request: UserCreateRequest) -> User:
        """ユーザー作成のハンドラ"""
        user = User(
            id=user_request.id,
            name=user_request.name,
            personality=user_request.personality or "You are an assistant that speaks like a cute girlfriend."
        )
        return self.user_service.create_user(user)

    def handle_get_user(self, user_id: str) -> User:
        """ユーザー取得のハンドラ"""
        return self.user_service.get_user(user_id)

    def handle_update_personality(self, user_id: str, personality: str) -> User:
        """ユーザーの性格設定更新のハンドラ"""
        return self.user_service.update_user_personality(user_id, personality)
