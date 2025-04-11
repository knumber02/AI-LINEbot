from fastapi import APIRouter, HTTPException
from api.models.user import User
from api.state import users
import openai
from api.handlers.user_handler import handle_create_user, handle_get_user, handle_update_personality

router = APIRouter()

@router.post("/users/")
def create_user(user: User):
    return handle_create_user(user)

@router.get("/users/{user_id}")
def read_user(user_id: str):
    return handle_get_user(user_id)

@router.put("/users/{user_id}/personality")
def set_personality(user_id: str, personality: str):
    return handle_update_personality(user_id, personality)
