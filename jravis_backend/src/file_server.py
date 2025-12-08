from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter()

@router.get("/{path:path}")
def serve_file(path: str):
    abs_path = os.path.join("factory_output", path)

    if not os.path.exists(abs_path):
        return {"error": "File not found"}

    return FileResponse(abs_path)
