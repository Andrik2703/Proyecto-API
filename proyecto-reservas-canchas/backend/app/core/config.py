from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # Database - usar SQLite por defecto
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sportreserva.db")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "tu_clave_secreta_cambiar_en_produccion")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()