"""
Configuration de l'application Neuropath
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Application
    app_name: str = "Neuropath"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str = "sqlite:///./neuropath.db"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    max_tokens: int = 2000
    
    # Scraping
    scraping_timeout: int = 30
    selenium_headless: bool = True
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Paths
    base_dir: Path = Path(__file__).parent.parent
    data_dir: Path = base_dir / "data"
    reports_dir: Path = base_dir / "reports"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance globale des settings
settings = Settings()

# Créer les dossiers nécessaires
settings.data_dir.mkdir(exist_ok=True)
settings.reports_dir.mkdir(exist_ok=True)
