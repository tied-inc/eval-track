from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    EVAL_TRACKER_BASE_URL: str = Field(..., description="tracker api service url")
