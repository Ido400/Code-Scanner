from common.errors.dir_exsits import DirExists
from common.errors.dir_not_found import DirNotFound
from common.errors.file_not_found import FileNotFound


class FileSystem:
    def __init__(self, path:str) -> None:
        self.path = path
    
    def create_dir(self, dir_name:str) -> None:
        import os
        import shutil
        """
        This method will create a new dir.
        
        Args:
        -----
            dir_name(str): The name of the dir
        """
        try:
            os.mkdir(f"{self.path}/{dir_name}")
            shutil.copy(f"{self.path}/plugins.json", f"{self.path}/{dir_name}")
        except OSError:
            raise DirExists("The dir is not found")

    def create_file(self, dir_name:str, file_name:str, file_data:str) -> None:
        """
        This method will create new file.

        Args:
        -----
            dir_name(str): The name of dir name
            file_name(str): The name of the file
            file_data(str): The data of the file
        """
        try:
            with open(f"{self.path}/{dir_name}/{file_name}","w") as file:
                data = file_data
                file.write(data)
        except OSError:
           raise DirNotFound("The dir is not found")

    def read_data(self, dir_name:str, file_name:str) -> str:
        """
        This method will open the file and read the data.

        Args:
        -----
            dir_name(str): This is the name of the dir
            file_name(str): This is the name of of the file
        """
        try:
            data:str
            with open(f"{self.path}/{dir_name}/{file_name}", "r") as file:
                data = file.read()
            return data
        except OSError:
            FileNotFound("The file is not found")
 