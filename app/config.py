from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Application"
    DEBUG: bool = False
    DATABASE_URL: str = "sqlite:///./test.db"

    # Additional settings can be added here
    API_PREFIX: str = "/api"

    class Config:
        env_file = ".env"  # Load environment variables from a .env file if present

# Create an instance of the settings to be used throughout the app
settings = Settings()