from fastapi import APIRouter, HTTPException
from api.models.user import User
from api.state import users
import openai

router = APIRouter()

@router.post("/users/")
def create_user(user: User):
    if user.id not in users:
        users[user.id] = user
    return user

@router.get("/users/{user_id}")
def read_user(user_id: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@router.put("/users/{user_id}/personality")
def set_personality(user_id: str, personality: str):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[user_id].personality = personality
    return {"message": "Personality set successfully."} 
