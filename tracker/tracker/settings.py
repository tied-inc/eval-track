from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    eval_tracker_host: str = Field(default="0.0.0.0", description="tracker api service host")
    eval_tracker_port: int = Field(default=8000, description="tracker api service port")
    eval_tracker_secret_key: str = Field(default="", description="tracker api service secret key")
    eval_tracker_trusted_hosts: list[str] = Field(default=[], description="tracker api service trusted hosts")

    @field_validator("eval_tracker_trusted_hosts", mode="before")
    @classmethod
    def decode_string_list_to_list(cls, v: str) -> list[str]:
        if isinstance(v, list):
            return v

        return v.split(",")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", enable_decoding=False)


settings = Settings()
