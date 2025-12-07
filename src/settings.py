import os

# ---------------------------------------------------
# LOAD ENVIRONMENT VARIABLES SAFELY
# ---------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY", "")
GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")
MESHY_API_KEY = os.getenv("MESHY_API_KEY", "")
WORKER_API_KEY = os.getenv("WORKER_API_KEY", "")

# ---------------------------------------------------
# BACKEND URL (worker calls backend using this)
# ---------------------------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "https://jravis-backend.onrender.com")

# ---------------------------------------------------
# UNIVERSAL OUTPUT FOLDER (used by publishers & engines)
# ---------------------------------------------------
OUTPUT_FOLDER = "generated_output"

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

SAFE_OUTPUT = os.path.join(OUTPUT_FOLDER, "default.txt")
if not os.path.exists(SAFE_OUTPUT):
    with open(SAFE_OUTPUT, "w") as f:
        f.write("JRAVIS default output placeholder.")

# ---------------------------------------------------
# EMAIL SETTINGS (shared by summary, invoices, newsletters)
# ---------------------------------------------------
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

# These MUST remain environment variables on Render
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

EMAIL_FROM = os.getenv("EMAIL_FROM", "elinalakshya@gmail.com")
