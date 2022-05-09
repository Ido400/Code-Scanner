import uvicorn
import motor
from fastapi import FastAPI
from beanie import init_beanie

from common.logging_controller import create_logger
create_logger("API_CLIENT")
#
from tools.routes import user,dir
from common.documents.user_document import User



MONGO_CONNECTION_STRING = "mongodb://root:Aa123456@localhost:27017/"

app = FastAPI()

app.include_router(user.router)
app.include_router(dir.router)

@app.on_event("startup")
async def app_init():
    client =  motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_STRING)
    await init_beanie(database=client.database_name, document_models=[User])


if __name__ == "_main_":
    uvicorn.run()