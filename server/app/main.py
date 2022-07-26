from fastapi import FastAPI, APIRouter

from app.app.api_v1 import api_router as v1_api_router


router = APIRouter()
router.include_router(v1_api_router)


def get_application() -> FastAPI:
    app = FastAPI(title="UNICN SERVER")
    app.include_router(router)
    return app


app = get_application()
