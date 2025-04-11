from fastapi import HTTPException
from api.models.user import User
from api.state import users

def handle_create_user(user: User) -> User:
    """ユーザー作成のハンドラ"""
    if user.id not in users:
        users[user.id] = user
    return user

def handle_get_user(user_id: str) -> User:
    """ユーザー取得のハンドラ"""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

def handle_update_personality(user_id: str, personality: str) -> dict:
    """ユーザーの性格設定更新のハンドラ"""
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].personality = personality
    return {"message": "Personality set successfully."}
