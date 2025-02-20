from fastapi import APIRouter

from .auth import auth_router
from .conversation import conversation_route
from .upload import upload_router
from .health import health_check_router

api_router = APIRouter()
api_router.include_router(router=auth_router, prefix="/auth")
api_router.include_router(router=upload_router, prefix="/upload")
api_router.include_router(router=conversation_route, prefix="/chat")
api_router.include_router(router=health_check_router, prefix="/heath")
