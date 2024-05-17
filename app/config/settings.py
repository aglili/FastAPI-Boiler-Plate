import os
from typing import List

from pydantic import AnyHttpUrl, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Selorms FastAPI Boiler-Plate"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = os.getenv(
        "BACKEND_CORS_ORIGINS",
        [
            "http://localhost:8000",
            "https://localhost:8000",
            "http://localhost",
            "https://localhost",
        ],
    )
    PROJECT_VERSION: str = "0.0.1"
    API_V1_STR: str = "/api/v1"

    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = os.getenv("DB_PORT", 5432)
    DB_USERNAME: str = os.getenv("DB_USERNAME", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    DB_NAME: str = os.getenv("DB_NAME", "boilerplate")
    DB_ENGINE: str = os.getenv("DB_ENGINE", "postgresql")

    DB_URI: str = "{db_engine}://{user}:{password}@{host}:{port}/{database}".format(
        db_engine=DB_ENGINE,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )

    PASSWORD_REGEX: str = os.getenv(
        "PASSWORD_REGEX",
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{8,}$",
    )
    SECRET_KEY: str = os.getenv("SECRET_KEY", "test_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
