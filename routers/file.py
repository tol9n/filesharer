from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from utils import convert_path
from s3 import Manager

s3_manager = Manager('tol9nteststorage')
file_router = APIRouter(prefix="/files")

@file_router.get("/{filepath}/{filename}")
async def get_image(filepath: str, filename: str) -> StreamingResponse:
    key = convert_path(filepath, filename)
    response = await s3_manager.get_object_by_name(key)
    return StreamingResponse(response, media_type="image/jpeg")

@file_router.get('/get_files_list')
async def get_files_list():
    response = await s3_manager.get_object_list()
    print(response)
    return response