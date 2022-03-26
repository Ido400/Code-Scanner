from dataclasses import dataclass

@dataclass
class Mongo:
    host:str
    username:str
    password:str
    port:str
    db:str
    
    def get_mongo_client(self):
        return f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/"