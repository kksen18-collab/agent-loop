from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings


class AgentLoopSettings(BaseSettings):
    openai_api_key: str
    model: str = "gpt-5.2"

    model_config = {
        "env_file": Path(__file__).parent / ".env",
    }

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v):
        if not v.startswith("sk-"):
            raise ValueError("invalid openai api key")
        return v
