from pydantic import BaseModel,Field
from typing import Optional


class User(BaseModel):
    user_id:Optional[str]=Field(..., allow_mutation=False)
    user_name:str
    folders:list
    engines:Optional[dict]

    class Config:
        validate_assignment = True