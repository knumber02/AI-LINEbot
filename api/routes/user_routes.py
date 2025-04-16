from fastapi import APIRouter, HTTPException, Depends
from api.requests.user import UserCreateRequest, UserPersonalityUpdateRequest
from api.models.user import User
from api.responses.error import ErrorResponse
from api.handlers.user_handler import UserHandler
from typing import Annotated, List, Optional
from sqlalchemy.orm import Session
from api.database import get_db
from api.responses.user import UserResponse
from api.repositories.interfaces.user_repository_interface import IUserRepository
from api.repositories.user_repository import UserRepository
from api.services.user_service import UserService

router = APIRouter()

def get_repository(db: Annotated[Session, Depends(get_db)]) -> IUserRepository:
    return UserRepository()

def get_service(repository: Annotated[IUserRepository, Depends(get_repository)]) -> UserService:
    return UserService(repository)

def get_handler(service: Annotated[UserService, Depends(get_service)]) -> UserHandler:
    return UserHandler(service)

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
    user_handler: Annotated[UserHandler, Depends(get_handler)],
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
    user_handler: Annotated[UserHandler, Depends(get_handler)],
    db: Annotated[Session, Depends(get_db)]
):
    return user_handler.handle_get_user(user_id, db)

# todo: ユーザーではなく、キャラクター性格設定のAPIを作成する
# @router.put(
#     "/{user_id}/personality",
#     response_model=UserResponse,
#     responses={
#         404: {"model": ErrorResponse},
#         500: {"model": ErrorResponse}
#     },
#     description="ユーザーの性格を更新します"
# )
# def set_personality(
#     user_id: str,
#     personality_update: UserPersonalityUpdateRequest,
#     user_handler: Annotated[UserHandler, Depends(UserHandler)],
#     db: Annotated[Session, Depends(get_db)]
# ):
#     return user_handler.handle_update_personality(user_id, personality_update.personality, db)
