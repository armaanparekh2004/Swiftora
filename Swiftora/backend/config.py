"""Application configuration handling for Swiftora's backend.

This module centralises reading environment variables and provides a
convenient `Settings` object.  It relies on pydantic so that types are
validated at runtime and defaults are applied when variables are not
defined.  The optional `.env` file can be used for local overrides.
"""

from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field
from dotenv import load_dotenv


# Load environment variables from a local .env file if present.  This
# call is idempotent and harmless if the file does not exist.
load_dotenv()


class Settings(BaseSettings):
    """Settings for the Swiftora backend.

    The configuration is read from environment variables.  See
    `.env.example` for a list of supported variables.
    """

    demo_mode: bool = Field(True, env="DEMO_MODE")
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ebay_client_id: Optional[str] = Field(None, env="EBAY_CLIENT_ID")
    ebay_client_secret: Optional[str] = Field(None, env="EBAY_CLIENT_SECRET")
    firebase_api_key: Optional[str] = Field(None, env="FIREBASE_API_KEY")
    log_level: str = Field("info", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return a cached `Settings` instance.

    The use of `lru_cache` ensures that environment variables are parsed
    only once per process lifetime.  Subsequent calls return the same
    object.
    """

    return Settings()  # type: ignore