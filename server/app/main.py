from fastapi import FastAPI

from app.app.api_v1 import api_router


def get_application() -> FastAPI:
    app = FastAPI(title="UNICN SERVER")
    app.include_router(api_router)
    return app


app = get_application()
