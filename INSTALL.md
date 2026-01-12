# Guide d'Installation - Neuropath

## Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- Chrome/Chromium (pour Selenium, optionnel)

## Installation

### 1. Cloner le projet (si applicable)

```bash
cd Neuropath
```

### 2. Créer un environnement virtuel (recommandé)

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configuration

Copiez le fichier `.env.example` vers `.env` :

```bash
cp .env.example .env
```

Éditez `.env` et configurez votre clé API OpenAI :

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Note:** L'API OpenAI est optionnelle. Sans clé API, seule l'analyse basique (pattern matching) fonctionnera.

### 5. Installation de ChromeDriver (pour Selenium, optionnel)

Si vous voulez utiliser Selenium pour scraper les sites JavaScript :

- Téléchargez ChromeDriver depuis https://chromedriver.chromium.org/
- Ajoutez-le à votre PATH
- Ou utilisez webdriver-manager (à ajouter dans requirements.txt si nécessaire)

## Démarrage

### Démarrer le serveur API

```bash
python run.py
```

Ou directement avec uvicorn :

```bash
uvicorn src.api.main:app --reload
```

Le serveur sera accessible sur `http://localhost:8000`

### Utiliser l'interface web

1. Ouvrez `frontend/index.html` dans votre navigateur
2. Ou servez-le avec un serveur HTTP simple :

```bash
cd frontend
python -m http.server 8080
```

Puis ouvrez `http://localhost:8080`

## Utilisation de l'API

### Documentation interactive

Une fois le serveur démarré, visitez :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

### Exemple d'utilisation

```python
import requests

response = requests.post("http://localhost:8000/analyze", json={
    "url": "https://example.com",
    "use_selenium": False
})

result = response.json()
print(result)
```

## Structure du projet

```
Neuropath/
├── src/
│   ├── api/           # API FastAPI
│   ├── analyzer/      # Analyseur de biais
│   ├── database/      # Base de données des biais
│   ├── reports/       # Génération de rapports
│   └── scraper/       # Scraper web
├── frontend/          # Interface web
├── reports/           # Rapports générés
├── requirements.txt   # Dépendances Python
└── README.md          # Documentation principale
```

## Dépannage

### Erreur: "No module named 'openai'"

```bash
pip install openai
```

### Erreur: "ChromeDriver not found"

Installez ChromeDriver ou désactivez Selenium (utilisez `use_selenium: false`)

### Erreur: "OpenAI API key not found"

Configurez votre clé API dans le fichier `.env` ou l'analyse basique fonctionnera sans IA.
