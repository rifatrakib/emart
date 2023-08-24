from fastapi import FastAPI
from server.config.factory import settings
from server.routes.auth.v1 import router as auth_router

app = FastAPI()

app.include_router(auth_router)


@app.get("/health")
async def health_check():
    return {"app_name": settings.APP_NAME}
