import grequests
import requests

from common.read_data_strategy import ReadData

class ManageFolder:
    def __init__(self, url:str) -> None:
        self.url = url
    
    def create_dir(self, dir_name:str) -> None:
        data = {"dir_name": dir_name}
        requests.post(f"{self.url}/dir", json=data)
   
    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        data = {"dir_name":dir_name, "file_name":file_name, "file_data":file_data}
        requests.post(f"{self.url}/file", json=data)

    async def read_data(self, dir_name:str, file_name:str, strategy:ReadData) -> bytes:
        import json
        data = {"dir_name":dir_name, "file_name":file_name}
        response = requests.get(f"{self.url}/file", json=data)
        data =  strategy.read_data(response.text)
        return data
    
