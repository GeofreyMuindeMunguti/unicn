import os
from typing import Union, List, Optional, Dict, Any

from pydantic.class_validators import validator
from pydantic.env_settings import BaseSettings
from pydantic.networks import AnyHttpUrl, AnyUrl, PostgresDsn, RedisDsn

CURRENT_DIR = os.path.dirname(__file__)


class Settings(BaseSettings):
    APP_ENVIRONMENT: str = "development"
    APP_V1_STR: str = "app/v1/"
    CLIENT_ID: str
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    ACCESS_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24 * 7
    REFRESH_TOKEN_EXPIRY_IN_SECONDS: int = 60 * 60 * 24 * 7
    SECRET_KEY: str = "secret-key"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = 1234
    SMTP_HOST: Optional[str] = "test"
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = "info@unicn.com"
    EMAILS_FROM_NAME: Optional[str] = "UNICN"
    EMAILS_ENABLED: bool = True

    # REDIS settings
    REDIS_HOST: Optional[str] = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    REDIS_SOCKET_TIMEOUT: Optional[float] = None

    # Celery settings
    CELERY_BROKER: Optional[RedisDsn] = None

    @validator("CELERY_BROKER", pre=True)
    def assemble_celery_broker(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v

        return AnyUrl.build(
            scheme="redis",
            password=values.get("REDIS_PASSWORD"),
            host=values.get("REDIS_HOST"),
            port=f"{values.get('REDIS_PORT') or 6379}",
            path=f"/{values.get('REDIS_DB') or ''}",
        )

    CELERY_MAX_RETRIES: int = 3
    CELERY_INTERVAL: float = 0.2
    CELERY_MAIN_QUEUE: str = "main-queue"

    REGISTER_URL: str = "http://unicn.com/register"
    API_V1_STR: str = "/api/v1"
    JWT_ALGORITHM: str = "HS256"

    class Config:
        case_sensitive = True
