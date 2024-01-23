from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.events.openapi import app_metadata
from server.events.startup import lifespan


def main():
    app = FastAPI(lifespan=lifespan, **app_metadata())
    app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
    return app
