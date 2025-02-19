import secrets
from enum import Enum
from typing import Annotated, Any, List, Literal, Optional

from pydantic import AnyUrl, BeforeValidator, HttpUrl, PostgresDsn
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings


def parse_cors(v: Any) -> List[str] | str:
    """
    Parses CORS origins input into a list or returns the input as is.
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)


class AppEnvironment(str, Enum):
    """
    Enum for app environments.
    """

    LOCAL = "local"
    PREVIEW = "preview"
    PRODUCTION = "production"


class ApplicationSetting(BaseSettings):
    """
    Application settings.
    """

    PROJECT_NAME: str = "QLLM"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520
    UVICORN_WORKER_COUNT: Optional[int] = None
    BACKEND_CORS_ORIGINS: Annotated[
        List[AnyUrl] | str,
        BeforeValidator(parse_cors),
    ]
    STORAGE_DIR: str = "storage"

    FRONTEND_HOST: str
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    LOG_LEVEL: Literal["DEBUG", "INFO", "ERROR", "WARNING"] = "DEBUG"
    SENTRY_DSN: Optional[HttpUrl] = None

    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"

    # Database config
    DATABASE_URL: str

    # LLM Config
    LLM_TEMPERATURE: float = 0.5
    LLM_MAX_TOKENS: int | None = None  # Default or set a specific value
    EMBEDDING_DIM: int = 1536
    EMBEDDING_MODEL: Optional[str] = None

    # OpenAI Config
    LLM_OPENAI_MODEL: Optional[str] = "gpt-4o-mini"
    OPENAI_API_KEY: str

    # Qdrant Config
    ## Self-host
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    ## On cloud
    QDRANT_URL: Optional[str] = None
    QDRANT_API_KEY: Optional[str] = None
    COLLECTION_NAME: str = "document"

    # Deployment
    RENDER: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings
settings = ApplicationSetting()
