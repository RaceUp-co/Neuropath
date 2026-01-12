"""
Script pour démarrer le serveur Neuropath
"""
from src.api.main import app
from src.config import settings
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
