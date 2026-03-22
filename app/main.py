from fastapi import FastAPI
from app.api.v1.endpoints import todos
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/")
async def root():
    return {"message": "Chào mừng bạn đến với ứng dụng To-Do List!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(todos.router, prefix=settings.API_V1_STR + "/todos", tags=["todos"])
