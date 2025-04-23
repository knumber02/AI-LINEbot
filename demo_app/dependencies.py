from fastapi import Depends
from typing import Annotated
from sqlalchemy.orm import Session
from demo_app.db import get_db
from demo_app.repositories.user_repository import UserRepository
from demo_app.repositories.message_repository import MessageRepository
from demo_app.repositories.character_repository import CharacterRepository
from demo_app.services.user_service import UserService
from demo_app.services.line_service import LineService
from demo_app.services.chat_service import ChatService
from demo_app.handlers.user_handler import UserHandler
from demo_app.handlers.line_handler import LineHandler
from demo_app.repositories.interfaces.user_repository_interface import IUserRepository
from demo_app.repositories.interfaces.message_repository_interface import IMessageRepository
from demo_app.repositories.interfaces.character_repository_interface import ICharacterRepository
from demo_app.services.character_service import CharacterService
from demo_app.config import get_config

config = get_config()

# Repositories
def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> IUserRepository:
    return UserRepository()

def get_message_repository() -> IMessageRepository:
    return MessageRepository()

def get_character_repository() -> ICharacterRepository:
    return CharacterRepository()

# Services
def get_user_service(
    repository: Annotated[IUserRepository, Depends(get_user_repository)]
) -> UserService:
    return UserService(repository)

def get_line_service(
    user_service: UserService = Depends(get_user_service)
) -> LineService:
    return LineService(user_service)

def get_character_service(
    character_repository: ICharacterRepository = Depends(get_character_repository)
) -> CharacterService:
    return CharacterService(character_repository)

def get_chat_service(
    message_repository: IMessageRepository = Depends(get_message_repository),
    character_service: CharacterService = Depends(get_character_service)
) -> ChatService:
    return ChatService(
        api_key=config["OPENAI_API_KEY"],
        message_repository=message_repository,
        character_service=character_service,
    )

# Handlers
def get_user_handler(
    service: Annotated[UserService, Depends(get_user_service)]
) -> UserHandler:
    return UserHandler(service)

def get_line_handler(
    line_service: LineService = Depends(get_line_service),
    user_service: UserService = Depends(get_user_service),
    chat_service: ChatService = Depends(get_chat_service),
    db: Session = Depends(get_db)
) -> LineHandler:
    return LineHandler(line_service, user_service, chat_service, db) 
