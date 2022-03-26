from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def __init__(self, name:str,name_publish:str,name_consume:str) -> None:
        self.name = name
        self.name_publish = name_publish
        self.name_consume = name_consume
   
    @abstractmethod
    def send_to_engine(self, user_id:str,dir_name:str,file_name:str, rabbit:object) ->None:
        pass
   
    @abstractmethod
    def get_engine_metdata(self, user_id:str,path:str) -> dict:
        pass
    
    @abstractmethod
    def publish_engine(self, 
                            user_id:str, 
                            dir_name:str, 
                            file_name:str, 
                            status:str, 
                            rabbit:object)-> None:
        pass

    @abstractmethod
    def consume_engine(self, rabbit:object, func:callable)->None:
        pass
    
  