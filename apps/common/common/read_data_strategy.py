from abc import ABC, abstractmethod

class ReadData(ABC):
    @abstractmethod
    def read_data(self, data:str):
        pass