from pydantic import BaseModel
from typing import List, Dict

class User(BaseModel):
    id: str
    name: str
    personality: str = "You are an assistant that speaks like a cute girlfriend."
    messages: List[Dict[str, str]] = [] 
