import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

logger = logging.getLogger("uvicorn")


def mount_static_files(app: FastAPI, directory: str, path: str, html: bool = False):
    if os.path.exists(directory):
        logger.info(f"Mounting static files '{directory}' at '{path}'")
        app.mount(
            path,
            StaticFiles(directory=directory, check_dir=False, html=html),
            name=f"{directory}-static",
        )
