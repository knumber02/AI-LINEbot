from typing import Dict, List
from pydantic import BaseModel

class User(BaseModel):
    id: str
    name: str
    personality: str = "You are an assistant that speaks like a cute girlfriend."
    messages: List[dict] = []

users: Dict[str, User] = {'default': User(id='default', name='Default User', messages=[])}
