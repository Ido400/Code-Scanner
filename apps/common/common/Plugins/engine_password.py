from common.manage_rabbit import ManageRabbit
from common.publish.publish_basic import PublishBasic
from common.engine_scanner import Engine
from common.enums.dataclass_exchange import Exchange
from common.enums.datacalss_queue import Queue
from common.manage_engines import factory
exchange = Exchange("engines", "direct")

class PasswordEngine(Engine):
    name: "engine_password"
    name_key: "password_engine_key"
    name_publish: "password_engine_publish"
   
    def __init__(self, name:str) -> None:
        self.name = name
        self.name_publish = "password_engine_publish"
        self.queue = Queue(self.name, exchange, "password_engine_key")
      
    def send_to_engine(self,user_id:str ,dir_name:str, file_name:str, rabbit:ManageRabbit) -> None:
        import json 
        data = {"dir_name":dir_name, "file_name":file_name, "user_id":user_id}
        data = json.dumps(data)
        publish_strategy = PublishBasic()
        rabbit.publish(self.queue, publish_strategy, data)   
    
    def get_engine_metdata(self, path:str) -> dict:
        pass
    
    def publish_engine(self, user_id:str, dir_name:str, file_name:str, status:str ,rabbit:object) ->None:
        import json
        data = json.dumps({"user_id":user_id, "dir_name":dir_name, "file_name":file_name, "status":status})
        rabbit.send_to_queue(self.name_publish, data)
    
    def consume_engine(self, rabbit: object, func:callable):
        rabbit.receive(self.name, func)

    
def register() -> None:
    factory.register("engine_password", PasswordEngine)