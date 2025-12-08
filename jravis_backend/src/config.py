# -----------------------------------------------------------
# JRAVIS SETTINGS CONFIG (FINAL VERSION)
# -----------------------------------------------------------

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "JRAVIS Backend"
    VERSION: str = "1.0.0"

    # API KEYS
    REPORT_API_CODE: str = ""      # old key support
    WORKER_API_KEY: str = ""       # new worker auth key

    # Optional keys (future use)
    OPENAI_API_KEY: str = ""
    GUMROAD_API_KEY: str = ""
    PAYHIP_API_KEY: str = ""
    PRINTIFY_API_KEY: str = ""
    NEWSLETTER_API_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "allow"


# -----------------------------------------------------------
# IMPORTANT: create the exported settings object
# -----------------------------------------------------------
settings = Settings()
