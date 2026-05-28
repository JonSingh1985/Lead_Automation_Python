from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENROUTER_API_KEY: str
    API_BASE_URL: str = "https://openrouter.ai/api/v1/chat/completions"
    MAX_CONCURRENT_REQUESTS: int = 2

    class Config:
        env_file = ".env"

# Global config object

settings = Settings()