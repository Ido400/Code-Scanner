from typing import Any, Callable

from engine_scanner import Engine


class FactoryEngines:
    def __init__(self) -> None:
        self.engine_creator: dict[str, Callable[..., Engine]] = {}
    
    def register(self,engine_type:str, creator_fn:Callable[..., Engine]):
        self.engine_creator[engine_type] = creator_fn
    
    def unregister(self, engine_type:str):
        self.engine_creator.pop(engine_type, None)
 
    def create(self,arguments:dict):
        args_copy = arguments.copy()
        character_type = args_copy.pop("type")
        try:
            creator_func = self.engine_creator[character_type]
        except KeyError:
            raise ValueError(f"The Type {character_type} don't exits")
        return creator_func(**args_copy)

