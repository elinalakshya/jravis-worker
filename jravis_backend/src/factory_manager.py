from fastapi import APIRouter
from settings import settings
import os
import random
import zipfile

router = APIRouter()

# Create a fake template ZIP file
def create_zip(name):
    path = os.path.join(settings.FACTORY_DIR, f"{name}.zip")
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("content.txt", f"TEMPLATE: {name}")
    return path

@router.post("/generate")
def generate_template():
    name = f"template-{random.randint(1000, 9999)}"
    zip_path = create_zip(name)
    return {"status": "generated", "name": name, "zip": f"factory_output/{name}.zip"}

@router.post("/scale/{name}")
def scale_template(name: str):
    return {"status": "scaled", "name": name}
