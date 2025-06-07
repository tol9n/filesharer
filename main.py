import uvicorn
from fastapi import FastAPI

from routers.image import image_router


app = FastAPI()
app.include_router(image_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)