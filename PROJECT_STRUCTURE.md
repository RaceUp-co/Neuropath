# Structure du Projet Neuropath

## Vue d'ensemble

```
Neuropath/
├── src/                    # Code source principal
│   ├── api/               # API FastAPI
│   │   ├── main.py        # Application FastAPI principale
│   │   └── models.py      # Modèles Pydantic
│   ├── analyzer/          # Module d'analyse
│   │   └── bias_analyzer.py  # Analyseur de biais psychologiques
│   ├── database/          # Base de données des biais
│   │   └── biases.json    # 35+ biais psychologiques avec exemples UX
│   ├── reports/           # Génération de rapports
│   │   └── report_generator.py  # Générateur de rapports
│   ├── scraper/           # Module de scraping
│   │   └── web_scraper.py # Scraper web (BeautifulSoup + Selenium)
│   ├── config.py          # Configuration de l'application
│   └── __init__.py
├── frontend/              # Interface web
│   └── index.html         # Interface utilisateur HTML/JS
├── reports/               # Rapports générés (créé automatiquement)
├── data/                  # Données temporaires (créé automatiquement)
├── main.py               # Point d'entrée alternatif
├── run.py                # Script de démarrage principal
├── test_example.py       # Exemple de test
├── requirements.txt      # Dépendances Python
├── .env.example          # Exemple de configuration
├── README.md             # Documentation principale
├── INSTALL.md            # Guide d'installation
├── QUICKSTART.md         # Guide de démarrage rapide
└── LICENSE               # Licence Apache 2.0
```

## Modules Principaux

### 1. Scraping (`src/scraper/`)

**web_scraper.py**: Extrait le contenu des sites web
- BeautifulSoup pour sites statiques
- Selenium pour sites JavaScript (optionnel)
- Extrait: HTML, CSS, texte, titres, CTAs, images, liens, navigation, prix, formulaires

### 2. Analyse (`src/analyzer/`)

**bias_analyzer.py**: Détecte les biais psychologiques
- Analyse basique: pattern matching (fonctionne sans IA)
- Analyse IA: OpenAI GPT-4 (optionnel, nécessite clé API)
- Corrèle les éléments du site avec la base de données de biais
- Génère des scores et preuves

### 3. Base de données (`src/database/`)

**biases.json**: Base de données de 35+ biais psychologiques
- Chaque biais contient: nom, description, exemples UX, patterns de détection, impact, recommandations
- Biais couverts: ancrage, preuve sociale, surcharge de choix, effet halo, confirmation, aversion à la perte, rareté, etc.

### 4. Rapports (`src/reports/`)

**report_generator.py**: Génère des rapports d'analyse
- Rapports JSON structurés
- Rapports HTML formatés
- Résumés, scores, recommandations prioritaires
- Sauvegarde dans `reports/`

### 5. API (`src/api/`)

**main.py**: API REST FastAPI
- `/analyze`: Analyse d'un site web
- `/chat`: Interface de chat pour questions
- `/biases`: Liste des biais disponibles
- `/health`: Vérification de santé
- Documentation interactive: `/docs`

**models.py**: Modèles Pydantic pour validation

### 6. Configuration (`src/config.py`)

**Settings**: Configuration centralisée
- Variables d'environnement via `.env`
- Configuration serveur, OpenAI, scraping, etc.

### 7. Interface Web (`frontend/`)

**index.html**: Interface utilisateur moderne
- Saisie d'URL
- Affichage des résultats
- Chat interactif
- Design responsive

## Flux d'Exécution

1. **Utilisateur soumet une URL** (via interface web ou API)
2. **Scraping**: Le scraper extrait le contenu du site
3. **Analyse**: L'analyseur détecte les biais (basique + IA optionnel)
4. **Rapport**: Génération du rapport avec scores et recommandations
5. **Retour**: Résultats affichés à l'utilisateur

## Points d'Entrée

- **run.py**: Démarrage du serveur API (recommandé)
- **main.py**: Point d'entrée alternatif
- **test_example.py**: Exemple de test en ligne de commande

## Dépendances Principales

- **FastAPI**: Framework API REST
- **BeautifulSoup4**: Parsing HTML
- **Selenium**: Scraping JavaScript (optionnel)
- **OpenAI**: Intégration IA (optionnel)
- **Pydantic**: Validation de données
- **Loguru**: Logging

## Fichiers de Configuration

- **.env**: Variables d'environnement (à créer depuis .env.example)
- **requirements.txt**: Dépendances Python
- **src/config.py**: Configuration par défaut

## Dossiers Générés

- **reports/**: Rapports d'analyse générés
- **data/**: Données temporaires
- Ces dossiers sont créés automatiquement au premier lancement
