from fastapi import APIRouter, HTTPException, Depends
from api.models.user import User
from api.state import users
import openai
from api.handlers.user_handler import UserHandler
from typing import Annotated
router = APIRouter()

@router.post("/users/")
def create_user(user: User, user_handler: Annotated[UserHandler, Depends(UserHandler)]):
    return user_handler.handle_create_user(user)

@router.get("/users/{user_id}")
def read_user(user_id: str, user_handler: Annotated[UserHandler, Depends(UserHandler)]):
    return user_handler.handle_get_user(user_id)

@router.put("/users/{user_id}/personality")
def set_personality(user_id: str, personality: str, user_handler: Annotated[UserHandler, Depends(UserHandler)]):
    return user_handler.handle_update_personality(user_id, personality)
