from fastapi import APIRouter, HTTPException, BackgroundTasks

from common.documents.user_document import User
from common.enums.dataclass_rabbit import RabbitMQ
from common.manage_engines import ManageEngines
from common.manage_folder import ManageFolder
from common.enums.pydantic_file import File

router = APIRouter(prefix="/dir")

URL = "http://localhost:6000/"

rabbit_setup = RabbitMQ(host="localhost", username="guest", password="guest")

def create_file_background_task(file:File):
    """
    This method is a background task and it will create a new file.

    Args:
    ----
        file(File): This is a file object
    """
    manage_folder = ManageFolder(URL)
    manage_folder.create_file(file.dir_name, file.file_name, file.file_data)

def create_dir_background_task(dir:File):
    """
    This method will create a new dir.

    Args:
    -----
        dir(File): This is a file object
    """
    manage_folder = ManageFolder(URL)
    manage_folder.create_dir(dir.dir_name)

async def publish_engines_background_task(file:File, user:User):
    """
    This method will load all the desire engines and
    it will notify them about the new file.

    file(File): This is a file object
    user(User): This is a user object
    """
    manage_folder = ManageFolder(URL)
    manage_engines = ManageEngines(rabbit_setup, [])
    await manage_engines.load_engines(file.dir_name, manage_folder)
    manage_engines.engines_notify(user.user_name, file.dir_name, file.file_name)

@router.post("")
async def create_dir(file:File, user:User, background_tasks:BackgroundTasks):
    """
    Http Request:
       route:  /dir
       method: Post
       body:  File, user
    This method will create a new dir for specific user.
    """
    if(file.dir_name == ""):
        raise HTTPException(status_code=404, details="The dir name is not found.")
    if(user.user_name == ""):
        raise HTTPException(status_code=404, details="The username is not found.")
    background_tasks.add_task(create_dir_background_task, file)
    user_ = await User.find_one(User.user_name == user.user_name)
    if(file.dir_name not in user_.folders):
        user_.folders.append(file.dir_name)
        await user_.save()
  
@router.post("/file")
async def create_file(file:File, user:User, background_task:BackgroundTasks):
    """
    Http Request:
        route: /dir/file
        method: Post
        body: File, User
    This method will create a new file and notify the engines
    """
    if(file.dir_name == "" or file.file_name == ""):
        raise HTTPException(status_code=404, details="The dir name or file name not found")
    if(user.user_name == ""):
        raise HTTPException(status_code=404, details="The username is not found.")
    background_task.add_task(create_file_background_task, file)
    background_task.add_task(publish_engines_background_task, file, user)

@router.put("/file")
async def update_file(file:File, user:User,background_task:BackgroundTasks):
    """
    Http Request:
        route: /dir/file
        method: Put
        body: File, User
    This method will update the exist file.
    """
    if(file.dir_name == "" or file.file_name == ""):
        raise HTTPException(status_code=404, details="The dir name or file name not found")
    if(user.user_name == ""):
        raise HTTPException(status_code=404, details="The username is not found.")
    background_task.add_task(create_file_background_task, file)
    background_task.add_task(publish_engines_background_task, file, user)

@router.put("/engines")
async def update_engines(file:File, background_task:BackgroundTasks):
    """
    Http Request:
        route: /dir/engines
        method: Put
        body: File
    This method will update the engine plugin in the directory.
    """
    if(dir.dir_name == ""):
        raise HTTPException(status_code=404, details="The dir name is not found.")
    file.file_name= "plugins.json"
    file.file_data = file.file_plugins.json()
    background_task.add_task(create_file_background_task, file)

