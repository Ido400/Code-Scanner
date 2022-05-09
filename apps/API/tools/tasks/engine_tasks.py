from common.manage_folder import ManageFolder
from common.enums.pydantic_file import File
from common.documents.user_document import User
from common.enums.dataclass_rabbit import RabbitMQ
from common.manage_engines import ManageEngines

URL = "http://localhost:6000/"

async def publish_engines_background_task(file:File, user:User):
    """
    This method will load all the desire engines and
    it will notify them about the new file.

    file(File): This is a file object
    user(User): This is a user object
    """
    rabbit_setup = RabbitMQ(host="localhost", username="guest", password="guest")
    manage_folder = ManageFolder(URL)
    manage_engines = ManageEngines(rabbit_setup, [])
    await manage_engines.load_engines(file.dir_name, manage_folder)
    manage_engines.engines_notify(user.user_name, file.dir_name, file.file_name)