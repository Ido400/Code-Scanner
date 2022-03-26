from typing import Any, Callable

from common.engine_scanner import Engine


class FactoryEngines:
    def __init__(self) -> None:
        self.engine_creator: dict[str, Callable[..., Engine]] = {}
    
    def register(self,engine_type:str, creator_fn:Callable[..., Engine]):
        self.engine_creator[engine_type] = creator_fn
    
    def unregister(self, engine_type:str):
        self.engine_creator.pop(engine_type, None)
 
    def create(self,arguments:dict):
        args_copy = arguments.copy()
        print(args_copy)
        engine_name = args_copy.pop("name")
        try:
            creator_func = self.engine_creator[engine_name]
        except KeyError:
            raise ValueError(f"The Type {engine_name} don't exits")
        return creator_func(**arguments)

