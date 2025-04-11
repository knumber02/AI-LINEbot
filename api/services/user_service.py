from fastapi import HTTPException
from api.models.user import User
from api.requests.user import UserCreateRequest
from api.state import users
from typing import Optional

class UserService:
    def get_or_create_user(self, user_id: str) -> User:
        """ユーザーを取得または作成"""
        if user_id not in users:
            users[user_id] = User(id=user_id, name=None)
        return users[user_id]

    def get_user(self, user_id: str) -> User:
        """ユーザーを取得します"""
        user = users.get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, user: User) -> User:
        """ユーザーを作成します"""
        if user.id in users:
            return users[user.id]

        users[user.id] = user
        return user

    def update_user_personality(self, user_id: str, personality: str) -> User:
        """ユーザーの性格設定を更新します"""
        user = self.get_user(user_id)
        user.personality = personality
        return user
