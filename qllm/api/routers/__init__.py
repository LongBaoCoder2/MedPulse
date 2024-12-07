from fastapi import APIRouter

from .chat import chat_router
from .upload import upload_router

api_router = APIRouter()
api_router.include_router(router=chat, prefix="/chat")
api_router.include_router(router=upload, prefix="/upload")
