from fastapi import APIRouter

upload_router = r = APIRouter()


@r.post("")
async def post_upload_handler():
    return "UPLOAD"
