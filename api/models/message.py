from pydantic import BaseModel
from datetime import datetime

class Message(BaseModel):
    id: str
    user_id: str
    content: str
    created_at: datetime = datetime.now()
