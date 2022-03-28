from pydantic import BaseModel
from typing import List

from common.enums.pydantic_engine import Engine

class Engines(BaseModel):
    plugins:list
    engines:List[Engine]