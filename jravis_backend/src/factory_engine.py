import os, random

def create_template():
    os.makedirs("factory_output", exist_ok=True)
    name = f"template-{random.randint(1000,9999)}"
    zip_path = f"factory_output/{name}.zip"

    # Create placeholder ZIP
    with open(zip_path, "wb") as f:
        f.write(b"JRAVIS-ZIP-FILE")

    return {"status": "generated", "name": name, "zip": zip_path}

def scale_template(name: str):
    os.makedirs("factory_output", exist_ok=True)
    scaled = f"{name}-v{random.randint(100,999)}.zip"
    path = f"factory_output/{scaled}"

    with open(path, "wb") as f:
        f.write(b"SCALED-VARIANT")

    return {"status": "scaled", "name": name, "variant": path}
