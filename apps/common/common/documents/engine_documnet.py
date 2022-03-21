from pydantic import BaseModel,Field
from typing import Optional

class Engine(BaseModel):
    user_id:str=Field(..., allow_mutation=False)
    folder_name:str
    file_name:str
    description:str
    lines:Optional[list]
    
    class Config:
        validate_assignment = True

   
  

