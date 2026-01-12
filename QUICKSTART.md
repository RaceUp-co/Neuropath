# Guide de Démarrage Rapide - Neuropath

## Installation en 3 étapes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Configurer (optionnel)

Créez un fichier `.env` à la racine du projet :

```env
OPENAI_API_KEY=votre_cle_api_ici
```

**Note:** Sans clé API OpenAI, seule l'analyse basique (pattern matching) fonctionnera. C'est suffisant pour tester.

### 3. Démarrer le serveur

```bash
python run.py
```

Le serveur démarre sur `http://localhost:8000`

## Utilisation

### Option 1: Interface Web

1. Ouvrez `frontend/index.html` dans votre navigateur
2. Entrez une URL à analyser
3. Cliquez sur "Analyser"

### Option 2: API directement

```bash
# Tester l'API
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "use_selenium": false}'
```

### Option 3: Documentation Interactive

Visitez `http://localhost:8000/docs` pour la documentation Swagger interactive.

## Exemple Python

```python
import requests

# Analyser un site
response = requests.post("http://localhost:8000/analyze", json={
    "url": "https://example.com",
    "use_selenium": False
})

result = response.json()
print(f"Score global: {result['summary']['overall_score']}")
print(f"Biais détectés: {result['summary']['total_biases_detected']}")
```

## Fonctionnalités Disponibles

- ✅ Scraping web (BeautifulSoup + Selenium optionnel)
- ✅ Base de données de 35+ biais psychologiques
- ✅ Analyse automatique (pattern matching)
- ✅ Analyse IA (avec OpenAI API key)
- ✅ Génération de rapports
- ✅ Interface de chat
- ✅ API REST complète

## Dépannage Rapide

**Erreur: "No module named 'X'"**
→ `pip install -r requirements.txt`

**Erreur: "ChromeDriver not found"**
→ Désactivez Selenium (utilisez `use_selenium: false`) ou installez ChromeDriver

**L'analyse ne fonctionne pas**
→ Vérifiez que le serveur est démarré (`python run.py`)

**Pas d'analyse IA**
→ Normal si pas de clé API OpenAI. L'analyse basique fonctionne sans.
