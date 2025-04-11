from fastapi import HTTPException
from api.models.user import User
from api.state import users
from api.services.user_service import UserService


class UserHandler:
    def __init__(self):
        self.user_service = UserService()

    def handle_create_user(self, user: User) -> User:
        """ユーザー作成のハンドラ"""
        return self.user_service.create_user(user)

    def handle_get_user(self, user_id: str) -> User:
        """ユーザー取得のハンドラ"""
        return self.user_service.get_user(user_id)

    def handle_update_personality(self, user_id: str, personality: str) -> dict:
        """ユーザーの性格設定更新のハンドラ"""
        return self.user_service.update_user_personality(user_id, personality)
