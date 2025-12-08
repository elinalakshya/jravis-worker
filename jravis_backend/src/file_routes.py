from fastapi import APIRouter
from fastapi.responses import FileResponse
from settings import settings
import os

router = APIRouter()

@router.get("/factory_output/{file_name}")
def get_file(file_name: str):
    path = os.path.join(settings.FACTORY_DIR, file_name)
    if os.path.exists(path):
        return FileResponse(path)
    return {"error": "File not found"}
  
