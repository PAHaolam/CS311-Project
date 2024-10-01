import os
import enum
from llama_index.core.bridge.pydantic import BaseModel, Field
from decouple import config


class MessageRole(enum.Enum):
    user = "user"
    system = "system"


class Settings(BaseModel):
    type: str = Field(
        description="Type of llm",
        default="groq",
    )

    database_url: str = Field(
        default=config("DATABASE_URL"),
        description="Database URL to connect to",
    )

    llm: str = Field(description="Default LLM to use", default="llama3-8b-8192")

    number_of_msgs: int = Field(
        default=2,
        description="Number of history messages to be used to refine",
    )


setting = Settings()