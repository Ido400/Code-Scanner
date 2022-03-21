from itsdangerous import json
import requests
import json

from apps.common.common.read_data_strategy import ReadData

class ManageFolder:
    def __init__(self, url:str) -> None:
        self.url = url
    
    def create_dir(self, dir_name:str) -> None:
        data = {"dir_name": dir_name}
        data = json.dumps(data)
        requests.post(f"{self.url}/dir", data=data)
   
    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        data = {"dir_name":dir_name, "file_name":file_name, "file_data":file_data}
        data = json.dumps(data)
        requests.post(f"{self.url}/file", data=data)

    async def read_data(self, dir_name:str, file_name:str, strategy:ReadData) -> bytes:
        import json
        data = {"dir_name":dir_name, "file_name":file_name}
        data = json.dumps(data)
        response = requests.get(f"{self.url}/file", data=data)
        response = json.loads(response.text())["file_data"]
        return strategy.read_data(response)
    
