# Neuropath
Logiciel de calcul de pattern humain pour maximiser la visibilité d'un site internet

croisement des lois cognitive de base


Concept de Neuropath
Neuropath est un outil IA dédié à l'analyse des biais psychologiques humains dans les sites web pour optimiser l'UX et booster les conversions. Il cible des biais comme la confirmation, l'ancrage, l'aversion à la perte ou l'effet halo, qui influencent les décisions utilisateurs. Contrairement à un simple chatbot, il combine analyse automatisée et conseils actionnables pour guider les entreprises dans la création de sites plus intuitifs.
​

Fonctionnement Recommandé
Optez pour un programme d'analyse automatique hybride : l'utilisateur soumet une URL, l'outil scrape le site (HTML, CSS, textes), extrait éléments clés (titres, CTAs, layouts) et les corrèle à une base de biais psychologiques. Utilisez des LLMs comme GPT pour détecter patterns (ex. : couleurs d'urgence pour aversion à la perte) et générer un rapport avec scores et suggestions. Ajoutez une interface chat pour raffiner l'analyse ou poser des questions spécifiques.
​

Biais Ciblés pour Web Design
Ancrage : Prix initiaux élevés avant remise, faussant la perception de valeur.
​

Preuve sociale : Témoignages ou "X utilisateurs en ligne" pour conformité.
​

Surcharge de choix : Trop d'options causant paralysie décisionnelle.
​

Effet halo : Design visuel premium influençant la confiance globale.
​

Confirmation : Contenu renforçant croyances préexistantes, limitant exploration.
​

Étapes de Développement
Compilez une base de données de 50-100 biais avec exemples UX (utilisez listes existantes).
​

Implémentez scraping (Python avec BeautifulSoup/Selenium) et prompts IA pour matching (ex. : "Détecte biais d'ancrage dans ce CTA").

Générez rapports visuels : heatmaps d'attention prédites, scores par biais, fixes prioritaires (ex. : simplifier menu pour paradoxe du choix).
​

Testez sur sites réels, intégrez feedback loop via chat pour itérations.
​

Déployez comme SaaS avec API pour intégration Figma/WordPress.

Avantages pour Entreprises
Améliore conversions en rendant sites moins manipulateurs mais plus persuasifs psychologiquement. Réduit temps design via audits rapides (comme VisualEyes pour attention). Différencie votre agence en offrant audits "neuro-optimisés", avec ROI mesurable via A/B tests post-corrections.

## Installation et Démarrage

Voir [INSTALL.md](INSTALL.md) pour les instructions détaillées d'installation.

### Installation rapide

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
cp .env.example .env
# Éditer .env et ajouter votre OPENAI_API_KEY (optionnel)

# Démarrer le serveur
python run.py
```

### Utilisation

1. **Interface Web**: Ouvrir `frontend/index.html` dans votre navigateur
2. **API**: Le serveur API sera accessible sur `http://localhost:8000`
3. **Documentation API**: Visiter `http://localhost:8000/docs`

## Architecture

- **Scraping** (`src/scraper/`): Extraction du contenu web (HTML, CSS, texte)
- **Analyse** (`src/analyzer/`): Détection des biais psychologiques (pattern matching + IA)
- **Rapports** (`src/reports/`): Génération de rapports détaillés
- **API** (`src/api/`): API REST FastAPI
- **Base de données** (`src/database/`): 35+ biais psychologiques avec exemples UX

## Fonctionnalités

- ✅ Scraping web (BeautifulSoup + Selenium)
- ✅ Base de données de 35+ biais psychologiques
- ✅ Analyse automatique (pattern matching)
- ✅ Analyse IA (OpenAI GPT-4, optionnel)
- ✅ Génération de rapports (JSON + HTML)
- ✅ Interface de chat pour questions
- ✅ API REST complète
- ✅ Interface web moderne