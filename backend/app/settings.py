from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    FRONTEND_BASE: str = "http://localhost:3000"
    ENABLE_PAYWALL: bool = False
settings = Settings()