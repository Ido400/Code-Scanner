import logging
from typing import Callable
from common.logging_controller import exception
from common.engine_scanner import Engine

LOGGER = logging.getLogger(__name__)

class FactoryEngines:
    def __init__(self) -> None:
        self.engine_creator: dict[str, Callable[..., Engine]] = {}
    
    def register(self,engine_type:str, creator_fn:Callable[..., Engine]):
        """
        This method will register an new engine

        Args:
        -----
            engine_type(str): The name of engine
            creator_fn(Callable[...,Engine]): The engine object
        """
        self.engine_creator[engine_type] = creator_fn
    
    def unregister(self, engine_type:str):
        """
        This method will unregister an engine

        Args:
        -----
            engine_type(str): The name of the engine

        """
        self.engine_creator.pop(engine_type, None)
   
    @exception(LOGGER)
    def create(self,arguments:dict):
        """
        This method will create the engine 
        """
        args_copy = arguments.copy()
        engine_name = args_copy.pop("name")
        try:
            creator_func = self.engine_creator[engine_name]
            LOGGER.info(f"Import the plugin {engine_name}")
        except KeyError:
            raise ValueError(f"The Type {engine_name} don't exits")
        return creator_func(**arguments)

