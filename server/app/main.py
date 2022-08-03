from fastapi import FastAPI, APIRouter

from app.app.api_v1 import api_router as v1_api_router
from starlette.middleware.cors import CORSMiddleware


router = APIRouter()
router.include_router(v1_api_router)


def get_application() -> FastAPI:
    app = FastAPI(title="UNICN SERVER")

    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    return app


app = get_application()
