from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.config.factory import settings

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
async def health_check():
    return {"app_name": settings.APP_NAME}
