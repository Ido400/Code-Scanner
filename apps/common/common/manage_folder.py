import requests

from common.errors.dir_exsits import DirExists
from common.errors.dir_not_found import DirNotFound
from common.read_data_strategy import ReadData

class ManageFolder:
    def __init__(self, url:str) -> None:
        """
        Args:
        -----
            url(str): The url of the storage api
        """
        self.url = url
    
    def create_dir(self, dir_name:str) -> None:
        """
        This method will create a new dir.
        """
        data = {"dir_name": dir_name}
        response  = requests.post(f"{self.url}/dir", json=data)
        if(response == 400):
            raise DirExists(response.text)

    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        """
        This method will create new file
        """
        data = {"dir_name":dir_name, "file_name":file_name, "file_data":file_data}
        response = requests.post(f"{self.url}/file", json=data)
        if(response == 404):
            raise DirNotFound(response.text)

    async def read_data(self, dir_name:str, file_name:str, strategy:ReadData) -> bytes:
        """
        This method will read data

        Args:
        ------
            dir_name(str): The dir name.
            file_name(str): The file name.
            strategy(ReadData): The chosen strategy to read data.
        """
        data = {"dir_name":dir_name, "file_name":file_name}
        response = requests.get(f"{self.url}/file", json=data)
        if(response == 404):
            FileNotFoundError(response.text)
        data =  strategy.read_data(response.text)
        return data
    
