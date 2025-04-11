from fastapi import APIRouter, Depends
from api.requests.message import MessageCreate
from api.responses.message import MessageResponse
from api.responses.error import ErrorResponse
from api.handlers.message_handler import MessageHandler
from typing import Annotated, List

router = APIRouter()

@router.post(
    "/",
    response_model=MessageResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def create_message(
    message: MessageCreate,
    message_handler: Annotated[MessageHandler, Depends(MessageHandler)]
):
    return message_handler.handle_create_message(message)

@router.get(
    "/{user_id}",
    response_model=List[MessageResponse],
    responses={
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
def read_messages(
    user_id: str,
    message_handler: Annotated[MessageHandler, Depends(MessageHandler)]
):
    return message_handler.handle_get_messages(user_id)
