import os

def run_gumroad_engine(zip_path: str, template_name: str):
    """
    Gumroad publisher.
    MUST receive a FILE path, not a directory.
    """

    print(f"📦 Publishing to Gumroad → {template_name} Digital Asset")
    print(f"📤 Upload source = {zip_path}")

    if not os.path.isfile(zip_path):
        raise RuntimeError(f"Gumroad expected a file, got: {zip_path}")

    # ---- PLACEHOLDER FOR REAL GUMROAD API ----
    # with open(zip_path, "rb") as f:
    #     gumroad_api.upload(file=f, name=template_name)

    print("✅ Gumroad upload simulated successfully")
    return True
