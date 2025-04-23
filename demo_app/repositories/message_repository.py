from sqlalchemy.orm import Session
from demo_app.models.message import Message
from demo_app.repositories.interfaces.message_repository_interface import IMessageRepository

class MessageRepository(IMessageRepository):
    def create(self, user_id: int, character_id: int, content: str, role: str, db: Session) -> Message:
        message = Message(
            user_id=user_id,
            character_id=character_id,
            content=content,
            role=role
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_user_messages(self, user_id: int, limit: int, db: Session) -> list[Message]:
        return db.query(Message)\
            .filter(Message.user_id == user_id)\
            .order_by(Message.created_at.desc())\
            .limit(limit)\
            .all() 
