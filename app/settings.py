from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    SESSION_SECRET_KEY: str

    # MinIO Settings
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET: str = "chat-files"  # default value if not in .env

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()