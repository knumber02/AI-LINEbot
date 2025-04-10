from pydantic import BaseModel
from typing import List, Dict

class Character(BaseModel):
    id: str
    name: str
    age: int
    tone: str
    ending: str
    voice: str
    language: str
    personality: str
    messages: List[Dict[str, str]] = [] 
