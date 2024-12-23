from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    eval_tracker_base_url: str = Field(..., description="tracker api service url")

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_file=".env")
