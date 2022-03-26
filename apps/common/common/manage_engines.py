from common.enums.dataclass_rabbit import RabbitMQ
import common.loader  as loader
from common.factory_engines import FactoryEngines
from common.engine_scanner import Engine
from common.manage_folder import ManageFolder
from common.manage_rabbit import ManageRabbit, Rabbit
from common.read_json import ReadJson

factory = FactoryEngines()

class ManageEngines:
    def __init__(self, rabbit_setup:RabbitMQ, list_queues:list) -> None:
        self.engines = []
        self.rabbit = ManageRabbit(rabbit_setup, list_queues)
        
    async def load_engines(self, dir_name:str, manage_folder:ManageFolder):
        json_strategy = ReadJson()
        data = await manage_folder.read_data(dir_name, "plugins.json", json_strategy)
        loader.load_plugins(data["plugins"])
        self.engines = [factory.create(engine) for engine in data["engines"]]
        
    
    def engines_notify(self, user_id:str ,dir_name:str, file_name:str):
        for engine in self.engines:
            engine.send_to_engine(user_id,dir_name,file_name, self.rabbit)
   
    def engine_publish(self, user_id:str, path:str, status:str, engine:Engine):
        engine.publish_engine(user_id,path,status, self.rabbit)
        
    def engines_consume(self, engine:Engine, func:callable):
        engine.consume_engine(self.rabbit, func)

    
    