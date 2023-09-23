from fastapi import FastAPI
from server.config.factory import settings
from server.routes.account.v1 import router as account_router
from server.routes.auth.v1 import router as auth_router
from server.routes.profile.v1 import router as profile_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(account_router)
app.include_router(profile_router)


@app.get("/health")
async def health_check():
    return {"app_name": settings.APP_NAME}
