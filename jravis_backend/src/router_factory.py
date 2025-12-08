from fastapi import APIRouter
import uuid, os, zipfile

router = APIRouter()

@router.post("/generate")
def generate_template():
    name = f"template-{uuid.uuid4().hex[:4]}"
    folder = "factory_output"
    os.makedirs(folder, exist_ok=True)

    zip_path = f"{folder}/{name}.zip"

    # Create a real ZIP file with a placeholder file inside
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        placeholder_content = f"This is template {name}"
        zipf.writestr("content.txt", placeholder_content)

    return {"status": "generated", "name": name, "zip": zip_path}

@router.post("/scale/{name}")
def scale(name: str):
    return {"status": "scaled", "name": name}
