import os
from pathlib import Path

from jose.constants import ALGORITHMS


class Settings:

    PROJECT_TITLE: str = "DeviceBoard"
    PROJECT_VERSION: str = "0.0.1"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "password")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "db_device")
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"


    TIME_TO_EXPIRE:int = 10
    SECRET_KEY:str = "319f8cac9dca9641c32195e46d219d385c7322a081a23cbc81d110bbda91afc9"
    ALGORITHM:str = "HS256"

    TEST_USER_EMAIL = "test@example.com"

    ADMIN:int = 1
    MANAGER: int = 2
    USER: int = 3


settings = Settings()
