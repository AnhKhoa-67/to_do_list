from fastapi import FastAPI
from app.api.v1.endpoints import todos, auth
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)
# ... health check endpoints ...
app.include_router(auth.router, prefix=settings.API_V1_STR + "/auth", tags=["auth"])
app.include_router(todos.router, prefix=settings.API_V1_STR + "/todos", tags=["todos"])
