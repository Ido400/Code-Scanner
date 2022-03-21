import loader  as loader
from factory_engines import FactoryEngines
from engine_scanner import Engine
from manage_rabbitmq import Rabbit
from read_json import ReadJson

factory = FactoryEngines()

class ManageEngines:
    def __init__(self, host:str, username:str, password:str) -> None:
        self.engines = []
        self.rabbit = Rabbit(host,username,password)
        
    def load_engines(self, dir_name:str, manage_folder:object):
        json_strategy = ReadJson()
        data = manage_folder.read_data(dir_name, "plugins.json", json_strategy)
        loader.load_plugins(data["plugins"])
        self.engines = [factory.create(engine) for engine in data["engines"]]
    
    def engines_notify(self, user_id:str ,dir_name:str, file_name:str):
        for engine in self.engines:
            engine.send_to_engine(user_id,dir_name,file_name, self.rabbit)
   
    def engine_publish(self, user_id:str, path:str, status:str, engine:Engine):
        engine.publish_engine(user_id,path,status, self.rabbit)
        
    def engines_consume(self, engine:Engine):
        engine.consume_engine(self.rabbit)
