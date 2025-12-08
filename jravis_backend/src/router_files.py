from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/{file_path:path}")
def get_file(file_path: str):
    full = os.path.join("storage/files", file_path)
    if not os.path.exists(full):
        return {"error": "file not found"}

    return FileResponse(full)
