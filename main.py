"""
Point d'entrée principal pour Neuropath
"""
import uvicorn
from src.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
