from fastapi import FastAPI

from src.routers.incident import router

app = FastAPI()
app.include_router(router)
