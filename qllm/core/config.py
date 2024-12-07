import secrets
from enum import Enum
from typing import Annotated, Any, List, Literal

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
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins.
    # Example:
    # '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: Annotated[
        List[AnyUrl] | str,
        BeforeValidator(parse_cors),
    ] = []
    FRONTEND_HOST: str = "http://localhost:3000"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    LOG_LEVEL: Literal["DEBUG", "INFO", "ERROR", "WARNING"] = "DEBUG"
    SENTRY_DSN: HttpUrl | None = None

    # Database config
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""

    # LLM Config
    LLM_TEMPERATURE: float = 0.5
    LLM_MAX_TOKENS: int | None = None
    EMBEDDING_DIM: int = 1024
    EMBEDDING_MODEL: str | None = None

    # OpenAI Config
    LLM_OPENAI_MODEL: str | None = "gpt-4o-mini"
    OPENAI_API_KEY: str | None = None

    @property
    def UVICORN_WORKER_COUNT(self) -> int:
        """
        Returns the number of Uvicorn workers to use based on the environment.
        """
        if self.ENVIRONMENT == AppEnvironment.LOCAL:
            return 1
        # Recommended number of workers: (2 x $num_cores) + 1
        # Reference: https://docs.gunicorn.org/en/stable/design.html#how-many-workers
        return 3

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Builds the SQLAlchemy-compatible database URI.
        """
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


# Initialize settings
settings = ApplicationSetting()
