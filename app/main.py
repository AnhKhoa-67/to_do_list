from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.api.v1.endpoints import todos, auth
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(todos.router, prefix=settings.API_V1_STR + "/todos", tags=["todos"])

# Serve static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
