import logging

from common.enums.dataclass_rabbit import RabbitMQ
from common.errors.plugin_not_found import PluginNotFoundError
import common.loader  as loader
from common.factory_engines import LOGGER, FactoryEngines
from common.engine_scanner import Engine
from common.manage_folder import ManageFolder
from common.manage_rabbit import ManageRabbit
from common.read_json import ReadJson

factory = FactoryEngines()

class ManageEngines:
    def __init__(self, rabbit_setup:RabbitMQ, list_queues:list) -> None:
        self.engines = []
        self.rabbit = ManageRabbit(rabbit_setup, list_queues)
    
    async def load_engines(self, dir_name:str, manage_folder:ManageFolder):
        """
        This method will load the engines and create an engine object.

        Args:
        -----
            dir_name(str): The name of the dir
            manage_folder(ManageFolder): The manage folder object 
        """
        json_strategy = ReadJson()
        try:
            data = await manage_folder.read_data(dir_name, "plugins.json", json_strategy)
            loader.load_plugins(data["plugins"])
            self.engines = [factory.create(engine) for engine in data["engines"]]
        except FileNotFoundError:
            raise FileNotFoundError("The plugins file not found")
        except PluginNotFoundError:
            raise PluginNotFoundError("The plugin not found")
          
    def engines_notify(self, user_name:str ,dir_name:str, file_name:str):
        """
        This method will notify the engines about new file.

        Args:
        -----
            user_name(str): The user name index
            dir_name(str): The dir that store the file
            file_name(str): The file name that the client should scan 
        """
        for engine in self.engines:
            engine.send_to_engine(user_name,dir_name,file_name, self.rabbit)
   
    def engine_publish(self, user_id:str, path:str, status:str, engine:Engine):
        """
        """
        engine.publish_engine(user_id,path,status, self.rabbit)
        
    def engines_consume(self, engine:Engine, func:callable):
        engine.consume_engine(self.rabbit, func)

    
    