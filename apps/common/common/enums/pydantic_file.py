from typing import Optional
from pydantic import BaseModel

from common.enums.pydantic_engiens import Engines

class File(BaseModel):
    dir_name:str 
    file_name:Optional[str]
    file_data:Optional[str]
    file_plugins:Optional[Engines]