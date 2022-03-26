from abc import ABC, abstractmethod

class PublishStrategy(ABC):
    @abstractmethod
    def send_message(self, send_to_rabbit:callable, routing_key:str,
                            exchange:str, data:str):
        pass