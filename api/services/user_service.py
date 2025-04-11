from api.models.user import User
from api.state import users

class UserService:
    def get_user(self, user_id: str) -> User:
        if user_id not in users:
            raise ValueError("User not found")
        return users[user_id]

    def create_user(self, user_id: str, name: str, personality: str = "You are an assistant that speaks like a cute girlfriend.") -> User:
        if user_id in users:
            return users[user_id]

        user = User(
            id=user_id,
            name=name,
            personality=personality or "You are an assistant that speaks like a cute girlfriend."
        )
        users[user_id] = user
        return user

    def update_user_personality(self, user_id: str, personality: str) -> User:
        if user_id not in users:
            raise ValueError("User not found")

        user = users[user_id]
        user.personality = personality
        return user
