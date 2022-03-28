from abc import ABC, abstractmethod

class Engine(ABC):
    @abstractmethod
    def __init__(self, name:str) -> None:
        self.name = name
        
    @abstractmethod
    def send_to_engine(self, user_id:str,dir_name:str,file_name:str, rabbit:object) ->None:
        """
        This method responsible for notify the engine about new file
        """
        pass
   
    @abstractmethod
    def get_engine_metdata(self, user_id:str,path:str) -> dict:
        """
        This engine will get the engine data about the file
        """
        pass
    
    @abstractmethod
    def publish_engine(self, 
                            user_id:str, 
                            dir_name:str, 
                            file_name:str, 
                            status:str, 
                            rabbit:object)-> None:
        """
        This method will used by the engine to notify the master
        """
        pass

    @abstractmethod
    def consume_engine(self, rabbit:object, func:callable)->None:
        """
        This method consume data from the engine master queue
        """
        pass
    
  