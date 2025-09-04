import os
from datetime import timedelta


class Config:
    """Base configuration loaded from environment variables.

    Uses environment variables for secrets and database connectivity.
    """

    # Flask settings
    DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    TESTING = os.getenv("FLASK_TESTING", "false").lower() == "true"
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")

    # Database settings - prefer DATABASE_URL style; fallback to components.
    DATABASE_URL = os.getenv("DATABASE_URL")

    if not DATABASE_URL:
        DB_DIALECT = os.getenv("DB_DIALECT", "sqlite")
        DB_HOST = os.getenv("DB_HOST", "")
        DB_PORT = os.getenv("DB_PORT", "")
        DB_NAME = os.getenv("DB_NAME", os.path.join(os.getcwd(), "notes.db"))
        DB_USER = os.getenv("DB_USER", "")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")

        if DB_DIALECT == "sqlite":
            DATABASE_URL = f"sqlite:///{DB_NAME}"
        else:
            auth = f"{DB_USER}:{DB_PASSWORD}@" if DB_USER or DB_PASSWORD else ""
            port = f":{DB_PORT}" if DB_PORT else ""
            host = DB_HOST or "localhost"
            DATABASE_URL = f"{DB_DIALECT}://{auth}{host}{port}/{DB_NAME}"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Auth/JWT settings
    ACCESS_TOKEN_EXPIRES_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES", "60"))
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

    # OpenAPI
    API_TITLE = os.getenv("API_TITLE", "Notes API")
    API_VERSION = os.getenv("API_VERSION", "v1")
    OPENAPI_VERSION = os.getenv("OPENAPI_VERSION", "3.0.3")
    OPENAPI_URL_PREFIX = os.getenv("OPENAPI_URL_PREFIX", "/docs")
    OPENAPI_SWAGGER_UI_URL = os.getenv("OPENAPI_SWAGGER_UI_URL", "https://cdn.jsdelivr.net/npm/swagger-ui-dist/")

    @classmethod
    def access_token_timedelta(cls):
        return timedelta(minutes=cls.ACCESS_TOKEN_EXPIRES_MINUTES)
