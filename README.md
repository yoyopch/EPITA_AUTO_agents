# Agent LangChain — Assistant Financier

Projet de fin de TP — Agent intelligent basé sur LangChain avec des outils financiers, une base de données PostgreSQL, une interface web Streamlit et une API REST.

## Prérequis

- Python 3.12+
- Docker & Docker Compose
- Clé API OpenAI
- Clé API Tavily (pour la recherche web)

## Installation

### 1. créer l'environnement virtuel

```bash
cd EPITA_AUTO_agents
python -m venv venv
source venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configurer les variables d'environnement

```bash
cp .env.example .env
# Éditer .env et renseigner vos clés API
```

### 4. Lancer PostgreSQL avec Docker

```bash
# Si vous avez déjà une instance en cours, arrêtez-la d'abord
docker compose down -v
docker compose up -d
```

### 5. Initialiser la base de données

```bash
python init_db.py
python init_portfolio_db.py
```

## Utilisation

### Mode CLI (menu interactif)

```bash
python main.py
```

9 scénarios de test disponibles :
1. Consultation base de données (client)
2. Données financières (actions/crypto)
3. Calculs financiers multiples
4. Conversion de devises (API)
5. Calcul de prêt + intérêts
6. Recommandation personnalisée
7. Analyse de texte complète
8. Analyse financière multi-outils
9. Mémoire conversationnelle (3 questions enchaînées)

### Interface web Streamlit (C1)

```bash
streamlit run app.py
```

Ouvre automatiquement le navigateur sur `http://localhost:8501`.

### API REST (D1)

```bash
uvicorn api:app --reload
```
en général : `http://127.0.0.1:8000`
Endpoints :
- `POST /api/agent/query` — Interroger l'agent
  ```json
  {"question": "Quel est le cours de Apple ?"}
  ```
  Réponse :
  ```json
  {"response": "...", "tools_used": ["cours_action"]}
  ```
- `GET /api/health` — Vérifier que l'API est en ligne
- `GET /api/tools` — Lister les outils disponibles
- `GET /docs` — Documentation Swagger interactive
