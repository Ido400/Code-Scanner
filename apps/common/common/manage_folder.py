import requests
import logging

from common.errors.dir_exsits import DirExists
from common.errors.dir_not_found import DirNotFound
from common.read_data_strategy import ReadData
from common.logging_controller import exception

LOGGER = logging.getLogger(__name__)

class ManageFolder:
    def __init__(self, url:str) -> None:
        """
        Args:
        -----
            url(str): The url of the storage api
        """
        self.url = url
   
    @exception(LOGGER)
    def create_dir(self, dir_name:str) -> None:
        """
        This method will create a new dir.
        """
        data = {"dir_name": dir_name}
        response  = requests.post(f"{self.url}/dir", json=data)
        if(response.status_code == 400):
            raise DirExists(response.text)
        if(response.status_code == 200):
            LOGGER.info("Successfully create Directory")

    @exception(LOGGER)
    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        """
        This method will create a new file
        """
        data = {"dir_name":dir_name, "file_name":file_name, "file_data":file_data}
        response = requests.post(f"{self.url}/file", json=data)
        if(response.status_code == 404):
            raise DirNotFound(response.text)
        if(response.status_code == 200):
            LOGGER.info("Successfully create file")
    
    @exception(LOGGER)
    async def read_data(self, dir_name:str, file_name:str, strategy:ReadData) -> str:
        """
        This method send an http request to the storage api and get \n
        back the file data (str).

        Args:
        ------
            dir_name(str): The dir name.
            file_name(str): The file name.
            strategy(ReadData): The chosen strategy to read data.
        
        Returns:
        --------
            Return the file data in str
        """
        data = {"dir_name":dir_name, "file_name":file_name}
        response = requests.get(f"{self.url}/file", json=data)
        if(response.status_code == 404):
            FileNotFoundError(response.text)
        if(response.status_code == 200):
            LOGGER.info("Successfully read data from file")
            data =  strategy.read_data(response.text)
            return data
        
