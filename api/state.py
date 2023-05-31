from typing import Dict, List, Optional
from pydantic import BaseModel

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.messages = []


class Character:
    def __init__(self, id, age, tone, ending, voice, language, personality):
        self.id = id
        self.age = age
        self.tone = tone
        self.ending = ending
        self.voice = voice
        self.language = language
        self.personality = personality
        self.messages = []


users: Dict[str, User] = {'default': User(id='default', name='Default User')}
