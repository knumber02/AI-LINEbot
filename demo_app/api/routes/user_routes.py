from fastapi import APIRouter, HTTPException, Depends
from demo_app.requests.user import UserCreateRequest, UserPersonalityUpdateRequest
from demo_app.models.user import User
from demo_app.responses.error import ErrorResponse
from demo_app.handlers.user_handler import UserHandler
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from demo_app.db import get_db
from demo_app.responses.user import UserResponse
from demo_app.repositories.interfaces.user_repository_interface import IUserRepository
from demo_app.repositories.user_repository import UserRepository
from demo_app.services.user_service import UserService
from demo_app.dependencies import get_user_handler

router = APIRouter()

@router.post(
    "/",
    response_model=UserResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    description="ユーザーを作成します"
)
def create_user(
    user_request: UserCreateRequest,
    user_handler: Annotated[UserHandler, Depends(get_user_handler)],
    db: Annotated[Session, Depends(get_db)]
):
    return user_handler.handle_create_user(user_request, db)


@router.get(
    "/{user_id}",
    response_model=Optional[UserResponse],
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    description="ユーザーを取得します"
)
def get_user(
    user_id: str,
    user_handler: Annotated[UserHandler, Depends(get_user_handler)],
    db: Annotated[Session, Depends(get_db)]
):
    return user_handler.handle_get_user(user_id, db)
