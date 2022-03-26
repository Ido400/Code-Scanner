from msilib.schema import Class
from beanie import Document
from typing import Optional

class Engine(Document):
    user_id:str
    folder_name:str
    file_name:str
    description:str
    lines:Optional[list]
    
    class Collection:
        name = "engines"

