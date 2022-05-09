from common.manage_folder import ManageFolder
from common.enums.pydantic_file import File
from common.documents.user_document import User

URL = "http://localhost:6000/"

def create_file_background_task(file:File):
    """
    This method is a background task and it will create a new file.

    Args:
    ----
        file(File): This is a file object
    """
    manage_folder = ManageFolder(URL)
    manage_folder.create_file(file.dir_name, file.file_name, file.file_data)

def create_dir_background_task(dir:File, user:User):
    """
    This method will create a new dir.

    Args:
    -----
        dir(File): This is a file object
    """
    manage_folder = ManageFolder(URL)
    manage_folder.create_dir(f"{dir.dir_name}{user.user_name}")
