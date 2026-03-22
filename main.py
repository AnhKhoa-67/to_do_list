from fastapi import FastAPI

app = FastAPI(title="To-Do List API")

@app.get("/")
async def root():
    return {"message": "Chào mừng bạn đến với ứng dụng To-Do List!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}
