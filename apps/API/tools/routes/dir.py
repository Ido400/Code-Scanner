from fastapi import APIRouter, HTTPException, BackgroundTasks

from common.documents.user_document import User
from common.enums.pydantic_file import File

from tools.tasks.engine_tasks import publish_engines_background_task
from tools.tasks.folder_tasks import create_dir_background_task
from tools.tasks.folder_tasks import create_file_background_task

router = APIRouter(prefix="/dir")

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
    background_tasks.add_task(create_dir_background_task, file, user)
    user_ = await User.find_one(User.user_name == user.user_name)
    if(file.dir_name not in user_.folders):
        user_.folders.append(f"{file.dir_name}{user.user_name}")
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

