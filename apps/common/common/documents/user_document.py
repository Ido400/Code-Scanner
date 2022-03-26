from beanie import Document, Indexed
from typing import Optional


class User(Document):
    user_name:Indexed(str, unique=True)
    folders:Optional[list] = []
    engines:Optional[dict] = {}

    class Collection:
        name = "users"
