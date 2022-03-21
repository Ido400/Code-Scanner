from engine_scanner import Engine

class PasswordEngine(Engine):
    name: "password_engine"
    name_publish: "password_engine_publish"
    name_consume: "password_engine_consume"

    
    def __init__(self, name:str, name_publish:str, name_consume:str) -> None:
        self.name = name
        self.name_publish = name_publish
        self.name_consume = name_consume
        
    def send_to_engine(self,user_id:str ,dir_name:str, file_name:str, rabbit:object) -> None:
        import json 
        data = {"dir_name":dir_name, "file_name":file_name, "user_id":user_id}
        data = json.dumps(data)
        rabbit.send_to_queue(self.name, data)    
    
    def get_engine_metdata(self, path:str) -> dict:
        pass
    
    def publish_engine(self, user_id:str, dir_name:str, file_name:str, status:str ,rabbit:object) ->None:
        import json
        data = json.dumps({"user_id":user_id, "dir_name":dir_name, "file_name":file_name, "status":status})
        rabbit.send_to_queue(self.name_publish, data)
    
    def consume_engine(self, rabbit: object, func:callable):
        rabbit.receive(self.name, func)
