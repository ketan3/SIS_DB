from fastapi import FastAPI
from app.core.config import settings
from app.routers import register_routers

app = FastAPI(title=settings.PROJECT_NAME)

register_routers(app)

@app.get("/")
async def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME}"}