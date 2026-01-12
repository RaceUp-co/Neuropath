"""
API principale FastAPI pour Neuropath
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
from typing import Optional, List, Dict
from loguru import logger

from src.config import settings
from src.scraper.web_scraper import WebScraper
from src.analyzer.bias_analyzer import BiasAnalyzer
from src.reports.report_generator import ReportGenerator

# Initialisation de l'application
app = FastAPI(
    title="Neuropath API",
    description="API pour l'analyse des biais psychologiques dans les sites web",
    version=settings.app_version
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instances globales
scraper = WebScraper()
analyzer = BiasAnalyzer()
report_generator = ReportGenerator()


# Modèles Pydantic
class AnalysisRequest(BaseModel):
    url: HttpUrl
    use_selenium: Optional[bool] = False


class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None


class AnalysisResponse(BaseModel):
    url: str
    status: str
    report_id: Optional[str] = None
    summary: Optional[Dict] = None
    analysis: Optional[Dict] = None


# Endpoints
@app.get("/")
async def root():
    """Endpoint racine"""
    return {
        "name": "Neuropath API",
        "version": settings.app_version,
        "status": "running",
        "endpoints": {
            "analyze": "/analyze",
            "chat": "/chat",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {
        "status": "healthy",
        "openai_configured": settings.openai_api_key is not None
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_website(request: AnalysisRequest):
    """
    Analyse un site web pour détecter les biais psychologiques
    
    Args:
        request: Requête avec l'URL à analyser
        
    Returns:
        Résultats de l'analyse
    """
    try:
        url = str(request.url)
        logger.info(f"Début de l'analyse de {url}")
        
        # Scraping
        logger.info("Scraping du site...")
        scraped_data = scraper.scrape_url(url, use_selenium=request.use_selenium)
        
        # Analyse
        logger.info("Analyse des biais...")
        analysis_results = analyzer.analyze(scraped_data)
        
        # Génération du rapport
        logger.info("Génération du rapport...")
        report = report_generator.generate_report(url, scraped_data, analysis_results)
        
        return AnalysisResponse(
            url=url,
            status="completed",
            report_id=report.get('report_path', ''),
            summary=report.get('summary'),
            analysis=report.get('analysis')
        )
        
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'analyse: {str(e)}")


@app.post("/analyze/async")
async def analyze_website_async(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Analyse asynchrone d'un site web
    
    Args:
        request: Requête avec l'URL à analyser
        background_tasks: Tâches en arrière-plan
        
    Returns:
        Confirmation de démarrage
    """
    # TODO: Implémenter avec un système de queue (Redis, Celery, etc.)
    return {
        "status": "queued",
        "message": "L'analyse a été mise en file d'attente",
        "url": str(request.url)
    }


@app.get("/report/{report_id}")
async def get_report(report_id: str):
    """
    Récupère un rapport généré
    
    Args:
        report_id: ID du rapport
        
    Returns:
        Rapport complet
    """
    # TODO: Implémenter le stockage et récupération des rapports
    raise HTTPException(status_code=501, detail="Non implémenté")


@app.get("/report/{report_id}/html", response_class=HTMLResponse)
async def get_report_html(report_id: str):
    """
    Récupère un rapport en format HTML
    
    Args:
        report_id: ID du rapport
        
    Returns:
        Rapport HTML
    """
    # TODO: Implémenter
    raise HTTPException(status_code=501, detail="Non implémenté")


@app.post("/chat")
async def chat(chat_request: ChatMessage):
    """
    Interface de chat pour raffiner l'analyse
    
    Args:
        chat_request: Message du chat avec contexte optionnel
        
    Returns:
        Réponse du chat
    """
    try:
        # Utiliser l'IA pour répondre aux questions
        if not settings.openai_api_key:
            return {
                "response": "L'API OpenAI n'est pas configurée. Veuillez configurer OPENAI_API_KEY.",
                "status": "error"
            }
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.openai_api_key)
        except ImportError:
            return {
                "response": "Le package openai n'est pas installé.",
                "status": "error"
            }
        
        context_prompt = ""
        if chat_request.context:
            context_prompt = f"Contexte de l'analyse: {chat_request.context}"
        
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant expert en UX design et psychologie cognitive. Tu réponds aux questions sur l'analyse de sites web et les biais psychologiques."
                },
                {
                    "role": "user",
                    "content": f"{context_prompt}\n\nQuestion: {chat_request.message}"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {
            "response": response.choices[0].message.content,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Erreur lors du chat: {e}")
        return {
            "response": f"Erreur: {str(e)}",
            "status": "error"
        }


@app.get("/biases")
async def list_biases():
    """
    Liste tous les biais disponibles dans la base de données
    
    Returns:
        Liste des biais
    """
    import json
    from pathlib import Path
    
    biases_path = Path(__file__).parent.parent / "database" / "biases.json"
    try:
        with open(biases_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return {
                "total": len(data.get('biases', [])),
                "biases": data.get('biases', [])
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du chargement des biais: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
