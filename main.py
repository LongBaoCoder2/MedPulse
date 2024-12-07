import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from qllm.api.routers import api_router

# from qllm.core.utils import mount_static_files
from qllm.init_setting import init_openai

app = FastAPI()

init_openai()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api/v1")

# Mount the data files to serve the file viewer
# mount_static_files("data", "/api/files/data")
# Mount the output files from tools
# mount_static_files("output", "/api/files/output")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1", port=5601, reload=True)
