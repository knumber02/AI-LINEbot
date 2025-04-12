from pydantic import BaseModel
from typing import List, Dict, Optional

class User(BaseModel):
    id: str
    name: Optional[str] = None
    personality: str = "You are an assistant that speaks like a cute girlfriend."
    messages: List[Dict[str, str]] = []
    greeted: bool = False
