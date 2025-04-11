from fastapi import APIRouter, HTTPException, Depends
from api.requests.user import UserCreateRequest, UserPersonalityUpdateRequest
from api.models.user import User
from api.responses.error import ErrorResponse
from api.handlers.user_handler import UserHandler
from typing import Annotated, List

router = APIRouter()

@router.post(
    "/",
    response_model=User,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def create_user(
    user_request: UserCreateRequest,
    user_handler: Annotated[UserHandler, Depends(UserHandler)]
):
    return user_handler.handle_create_user(user_request)

@router.get(
    "/{user_id}",
    response_model=User,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def read_user(
    user_id: str,
    user_handler: Annotated[UserHandler, Depends(UserHandler)]
):
    return user_handler.handle_get_user(user_id)

@router.put(
    "/{user_id}/personality",
    response_model=User,
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def set_personality(
    user_id: str,
    personality_update: UserPersonalityUpdateRequest,
    user_handler: Annotated[UserHandler, Depends(UserHandler)]
):
    return user_handler.handle_update_personality(user_id, personality_update.personality)
