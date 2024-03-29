from fastapi import APIRouter, HTTPException   
from beanie.operators import Set
from pymongo.errors import DuplicateKeyError
import logging

LOGGER = logging.getLogger(__name__)

from common.documents.user_document import User

router = APIRouter(prefix="/user")

@router.post("")
async def add_user(user: User):
    """
    Http Request:
        route: /user
        method: Post
        body: User

    This method will insert a new User to the collection.
    """
    try:
        await user.insert()
        raise HTTPException(status_code=200, detail="Insert the username")
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="The username is exists")

@router.get("/{user_name}", response_model=User)
async def get_user(user_name: str) -> User:
    """
    Http Request:
        route: /user/{user_name}
        method: Get
        This method will return a User document.
    """
    try:
        user = await User.find_one(User.user_name == user_name)
        return user
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"The user name {user_name} not found")
   
@router.put("")
async def update_user(user_update: User):
    """
    Http Request:
        route: /user
        method: Put
        body: User
    This method will update the User in the collection
    """
    try:
        user = await User.find_one(User.user_name == user_update.user_name)
        user.folders = user_update.folders
        user.engines = user_update.engines
        await user.save()
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"The user name {user_update.user_name} not found")

@router.put("/upsert")
async def upsert_user(user: User):
    """
    Http Request:
        route: /user/upsert
        method: Put
        body: User
    This method will upsert the User.
    """
    await User.find_one(User.user_name == user.user_name).upsert(
        Set({User.engines:user.engines, User.folders:user.folders}),
        on_insert=user
    )
  
       

@router.delete("/{user_name}", response_model=User)
async def delete_user(user_name: str):
    """
    Http Request:
        route: /users/{users_name}
        method: Delete
    This method will delete the User.
    """
    try:
        user = await User.find_one(User.user_name == user_name)
        await user.delete()
    except AttributeError:
        raise HTTPException(status_code=404, detail=f"The user name {user_name} not found")
   