import logging
import sys
from contextlib import asynccontextmanager

import alembic
import uvicorn
from alembic import script
from alembic.config import Config
from alembic.runtime import migration
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from llama_index.core.node_parser.text.utils import split_by_sentence_tokenizer
from sqlalchemy.engine import Engine, create_engine

# from qllm.core.utils import mount_static_files
from qllm.api.routers import api_router
from qllm.core.config import AppEnvironment, settings
from qllm.core.vector_store import get_vector_store, run_init_vector_store
from qllm.init_setting import init_openai
from qllm.services.db.wait_for_db import check_database_connection

logger = logging.getLogger("uvicorn")


def check_current_head(alembic_cfg: Config, connectable: Engine) -> bool:
    directory = script.ScriptDirectory.from_config(alembic_cfg)
    with connectable.begin() as connection:
        context = migration.MigrationContext.configure(connection)
        return set(context.get_current_heads()) == set(directory.get_heads())


def __setup_logging(log_level: str):
    log_level = getattr(logging, log_level.upper())
    log_formatter = logging.Formatter(
        "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"
    )
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(log_formatter)
    root_logger.addHandler(stream_handler)
    logger.info("Set up logging with log level %s", log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    from pathlib import Path

    # first wait for DB to be connectable
    await check_database_connection()

    current_path = Path(__file__).parent
    cfg = Config(os.path.join(current_path, "alembic.ini"))
    # Change DB URL to use psycopg2 driver for this specific check
    db_url = str(settings.DATABASE_URL).replace(
        "postgresql+asyncpg://", "postgresql+psycopg2://"
    )
    script_location = cfg.get_main_option("script_location", "alembic")
    script_location = str(os.path.join(current_path, script_location))
    cfg.set_main_option("script_location", script_location)

    cfg.set_main_option("sqlalchemy.url", db_url)
    engine = create_engine(db_url, echo=True)
    if not check_current_head(cfg, engine):
        raise Exception(
            "Database is not up to date. Please run `poetry run alembic upgrade head`"
        )
    # initialize pg vector store singleton
    vector_store = get_vector_store()
    await run_init_vector_store()

    init_openai()

    try:
        # Some setup is required to initialize the llama-index sentence splitter
        # for checking dependencies
        split_by_sentence_tokenizer()
    except FileExistsError:
        # Sometimes seen in deployments, should be benign.
        logger.info("Tried to re-download NLTK files but already exists.")
    yield
    # This section is run on app shutdown
    await vector_store.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    lifespan=lifespan,
)


if settings.BACKEND_CORS_ORIGINS:
    logger.info("CORS enabled for %s", settings.BACKEND_CORS_ORIGINS)
    # origins = settings.BACKEND_CORS_ORIGINS.copy()
    origins = str(settings.BACKEND_CORS_ORIGINS)
    origins.append(settings.FRONTEND_HOST)
    # allow all origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_origin_regex="https://llama-app-frontend.*\.vercel\.app",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    origins = [
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
        "http://0.0.0.0",
    ]
    origins.append(settings.FRONTEND_HOST)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_PREFIX)


def start():
    """Launched with `poetry run start` at root level"""
    print("Running in AppEnvironment: " + settings.ENVIRONMENT)
    __setup_logging(settings.LOG_LEVEL)
    if settings.RENDER:
        # on render.com deployments, run migrations
        logger.debug("Running migrations")
        alembic_args = ["--raiseerr", "upgrade", "head"]
        alembic.config.main(argv=alembic_args)
        logger.debug("Migrations complete")
    else:
        logger.debug("Skipping migrations")
    live_reload = not settings.RENDER
    uvicorn.run(
        "qllm.main:app",
        host="0.0.0.0",
        port=8000,
        reload=live_reload,
        workers=settings.UVICORN_WORKER_COUNT,
    )
