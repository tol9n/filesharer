from fastapi import APIRouter
from fastapi.responses import FileResponse

image_router = APIRouter(prefix="/image")

@image_router.get("/{filepath}/{filename}")
async def get_image(filepath: str, filename: str) -> FileResponse:
    filename = filepath+'/'+filename
    return FileResponse(filename)