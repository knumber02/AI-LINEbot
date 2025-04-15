from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import registry

mapper_registry = registry()

# 新しい方式でBaseクラスを定義
class Base(DeclarativeBase):
    pass
