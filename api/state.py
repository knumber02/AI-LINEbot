from typing import Dict
from api.models.user import User
from api.models.character import Character
import json

# グローバルな状態管理
users: Dict[str, User] = {}
characters: Dict[str, Character] = {}

# デフォルトユーザーの初期化
default_user = User(id='default', name='Default User')
users['default'] = default_user

def initialize_default_character():
    """デフォルトキャラクターの初期化"""
    with open('/src/config.json') as f:
        config = json.load(f)
    
    default_character_config = config['default_character']
    characters["default"] = Character(
        id=default_character_config["id"],
        name=default_character_config["name"],
        age=default_character_config["age"],
        tone=default_character_config["tone"],
        ending=default_character_config["ending"],
        voice=default_character_config["voice"],
        language=default_character_config["language"],
        personality=default_character_config["personality"]
    )

# アプリケーション起動時にキャラクターを初期化
initialize_default_character()
