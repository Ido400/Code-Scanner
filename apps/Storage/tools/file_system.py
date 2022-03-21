class FileSystem:
    def __init__(self, path:str) -> None:
        self.path = path
    
    def create_dir(self, dir_name:str) -> None:
        import os
        import shutil
        os.mkdir(f"{self.path}/{dir_name}")
        shutil.copy(f"{self.path}/plugins.json", f"{self.path}/{dir_name}")
   
    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        with open(f"{self.path}/{dir_name}/{file_name}","a") as file:
            data = file_data.decode("utf-8") 
            file.write(data)

    def read_data(self, dir_name:str, file_name:str) -> bytes:
        data:bytes
        with open(f"{self.path}/{dir_name}/{file_name}", "rb") as file:
            data = file.read()
        return data.encode("utf-8")
    
 