from typing import Dict
from api.models.user import User
from api.models.character import Character

# グローバルな状態管理
users: Dict[str, User] = {}
characters: Dict[str, Character] = {}

# デフォルトユーザーの初期化
default_user = User(id='default', name='Default User')
users['default'] = default_user
