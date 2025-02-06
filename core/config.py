"""
---
"""

import os
import gnupg
from pathlib import Path
from dotenv import load_dotenv

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from pydantic import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    """---"""

    PROJECT_NAME: str = "TRANSPARÊNCIA API"
    PROJECT_VERSION: str = "0.0.1"
    PROJECT_DESCRIPTION: str = f"""..."""

    API_V1_STR: str = "/api/v1"

    DBBaseModel = declarative_base()
    
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv(
        "POSTGRES_PORT", "5432"
    )  # default POSTGRES port is 5432
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_URL = (
        "postgresql+asyncpg://"
        + f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    POSTGRES_URL_SYNC = (
        "postgresql://"
        + f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    ENV:str = os.getenv("ENV", "LOCAL")
    PORT:int = os.getenv("PORT")

    SECRET_KEY: str = os.getenv("SECRET_KEY")
    OTP_SECRET_KEY:str = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7


    class Config:
        """---"""

        case_sensitive = True

        def get_case_sensitive(self):
            """---"""
            return self.case_sensitive

        def set_case_sensitive(self, value):
            """---"""
            self.case_sensitive = value

    def get_project_name(self):
        """---"""
        return self.PROJECT_NAME

    def get_project_description(self):
        """---"""
        return self.PROJECT_DESCRIPTION


settings: Settings = Settings()
