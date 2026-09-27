import os
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CivicSense AI - SamAashwas"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")
    
    # AI Engine Thresholds
    DEDUPLICATION_RADIUS_METERS: float = float(os.getenv("DEDUPLICATION_RADIUS_METERS", "300.0"))
    DEDUPLICATION_SIMILARITY_THRESHOLD: float = float(os.getenv("DEDUPLICATION_SIMILARITY_THRESHOLD", "0.75"))
    
    # NLP & Vision Configuration
    NLP_MODEL_BACKEND: str = os.getenv("NLP_MODEL_BACKEND", "rule_hybrid")
    VISION_MODEL_BACKEND: str = os.getenv("VISION_MODEL_BACKEND", "civic_heuristic")
    
    # External APIs
    OPEN_METEO_API_URL: str = os.getenv("OPEN_METEO_API_URL", "https://api.open-meteo.com/v1/forecast")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    model_config = ConfigDict(case_sensitive=True)

settings = Settings()
