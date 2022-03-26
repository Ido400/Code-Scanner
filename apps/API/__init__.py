from fastapi import FastAPI
import uvicorn
from tools.routes import user

app = FastAPI()

app.include_router(user)

if __name__ == "__main__":
    uvicorn.run()