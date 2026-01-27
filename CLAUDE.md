# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexte du Projet

Projet OpenClassrooms #7 : API de prédiction de sentiments pour Air Paradis (compagnie aérienne fictive) visant à détecter le bad buzz sur Twitter en temps réel.

**Objectif** : Développer un prototype MLOps complet avec plusieurs approches de modélisation (classique, deep learning, BERT) et déploiement Cloud de l'API.

## Architecture du Projet

### Structure Globale

```
.
├── notebooks/          # Notebooks Jupyter d'expérimentation MLFlow
├── api/               # API FastAPI déployable
├── streamlit/         # Interface web de test avec monitoring PostHog
├── models/            # Modèles sérialisés
├── data/              # Données (non versionnées)
└── livrables/         # Documents de livraison
```

### Notebooks d'Expérimentation (ordre d'exécution)

1. **01_exploration_donnees.ipynb** : EDA du dataset Twitter (970k tweets)
2. **02_preprocessing.ipynb** : Prétraitement (lemmatization vs stemming) → génère CSV dans `data/processed/`
3. **03_modele_simple_logistique.ipynb** : Baseline avec TF-IDF + Régression Logistique
4. **04_modele_avance_deep_learning.ipynb** : Bi-LSTM et CNN avec Word2Vec/GloVe
5. **05_modele_bert.ipynb** : Fine-tuning BERT (transformers)

**Particularité** : Tous les notebooks utilisent MLFlow pour le tracking d'expérimentations (tracking URI configuré vers `file:///home/thomas/mlruns`).

### API de Production

L'API FastAPI (`api/app.py`) supporte **plusieurs types de modèles** via variables d'environnement :
- `MODEL_TYPE`: `bert`, `lstm`, `cnn`, ou `logistic`
- `MODEL_PATH`: chemin vers le modèle sérialisé

**Architecture API** :
- Endpoints : `/health`, `/predict`, `/predict/batch`, `/models`
- Validation Pydantic (max 280 caractères, max 100 tweets en batch)
- Chargement conditionnel TensorFlow/Transformers (fallback sur logistic si non disponibles)
- Support Docker et Heroku

### Interface Streamlit

L'application Streamlit (`streamlit/app.py`) :
- Consomme l'API FastAPI (URL configurable via `API_URL`)
- Tracking des erreurs avec **PostHog Analytics** (optionnel, désactivable)
- Permet validation manuelle des prédictions
- Visualisations interactives avec Plotly

**Important** : PostHog n'est utilisé QUE si `POSTHOG_API_KEY` est définie (Streamlit secrets ou env var). L'app fonctionne sans.

## Commandes de Développement

### Environnement Virtuel

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

### Installation des Dépendances

```bash
# Pour notebooks d'expérimentation
pip install -r requirements-full.txt

# Pour l'API uniquement
cd api && pip install -r requirements.txt

# Pour Streamlit uniquement
cd streamlit && pip install -r requirements.txt
```

### Lancer l'API Localement

```bash
cd api

# Avec modèle logistique (léger, pas de TensorFlow requis)
export MODEL_TYPE=logistic
export MODEL_PATH=./models/logistic_regression_model.pkl
python app.py

# Avec modèle BERT
export MODEL_TYPE=bert
export MODEL_PATH=./models/bert_sentiment_model
python app.py

# Ou avec uvicorn (auto-reload)
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera accessible à http://localhost:8000 (docs Swagger : http://localhost:8000/docs)

### Lancer Streamlit

```bash
cd streamlit

# Configurer l'URL de l'API
export API_URL=http://localhost:8000

streamlit run app.py
```

Interface accessible à http://localhost:8501

### MLFlow UI

```bash
# Depuis la racine du projet
mlflow ui --port 5001 --backend-store-uri file:///home/thomas/mlruns

# Ou avec le chemin du repo courant
mlflow ui --port 5001
```

UI accessible à http://localhost:5001 (affiche toutes les expérimentations trackées)

### Docker

```bash
cd api

# Build simple
docker build -t airparadis-api .

# Run avec montage volume pour les modèles
docker run -p 8000:8000 \
  -e MODEL_TYPE=bert \
  -v $(pwd)/../models:/app/models \
  airparadis-api

# Docker Compose (API + Streamlit + MLFlow)
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Tests

```bash
cd api

# Tests simples
pytest test_api.py -v

# Avec couverture
pytest test_api.py -v --cov=app --cov-report=html

# Test d'un endpoint spécifique
pytest test_api.py::TestPredictEndpoint -v

# Rapport de couverture : ouvrir htmlcov/index.html
```

**Note** : Les tests utilisent des mocks pour éviter de charger les vrais modèles TensorFlow/BERT (trop lourds).

## Points d'Attention pour le Développement

### Modèles et Sérialisation

- **Modèle logistique** : pickle (`.pkl`) avec scikit-learn + vectorizer TF-IDF
- **Modèles Deep Learning** : HDF5 (`.h5`) avec Keras + tokenizer joblib
- **BERT** : SavedModel TensorFlow + BertTokenizer (transformers)

Le tokenizer/vectorizer DOIT être sauvegardé avec le modèle et chargé à l'identique en production.

### Compatibilité TensorFlow

Le notebook 04 utilise `mixed_precision.set_global_policy("mixed_float16")` pour accélérer l'entraînement sur GPU. Désactiver si problèmes de compatibilité.

### Échantillonnage pour Développement

Dans `04_modele_avance_deep_learning.ipynb`, définir `SAMPLE_SIZE = 50_000` au lieu de `None` pour tester rapidement sans GPU (970k tweets = 2-3h d'entraînement).

### Variables d'Environnement Importantes

**API** :
- `MODEL_TYPE` : type de modèle (`bert`, `lstm`, `cnn`, `logistic`)
- `MODEL_PATH` : chemin vers le modèle
- `PORT` : port de l'API (défaut 8000)

**Streamlit** :
- `API_URL` : URL de l'API FastAPI (défaut `http://localhost:8000`)
- `POSTHOG_API_KEY` : clé PostHog (optionnel, peut être vide)
- `POSTHOG_HOST` : host PostHog (défaut `https://app.posthog.com`)

**MLFlow** :
- Le tracking URI est hardcodé dans les notebooks vers `file:///home/thomas/mlruns`. Adapter si nécessaire.

### Déploiement Heroku

L'API contient les fichiers nécessaires :
- `Procfile` : `web: uvicorn app:app --host 0.0.0.0 --port $PORT`
- `runtime.txt` : version Python
- `.slugignore` : exclusions pour réduire la taille du slug

Les modèles lourds (BERT) peuvent dépasser les limites gratuites. Privilégier le modèle logistique ou utiliser TensorFlow Lite.

### Monitoring en Production (Azure Application Insights)

Le projet mentionne Azure Application Insights pour :
- Tracer les tweets mal prédits
- Déclencher des alertes (3+ erreurs en 5 min)

**Implémentation actuelle** : PostHog est utilisé dans Streamlit pour tracer les feedbacks utilisateurs. Azure Insights non implémenté dans ce code.

## Critères d'Évaluation MLOps

Le projet doit démontrer :
1. ✅ **Tracking MLFlow** : expérimentations, métriques, artefacts (notebooks)
2. ✅ **Versioning Git** : historique avec 3+ commits distincts
3. ✅ **Pipeline CI/CD** : déploiement continu API sur Cloud (Heroku)
4. ✅ **Tests unitaires** : pytest avec mocks (`test_api.py`)
5. ✅ **API REST** : FastAPI indépendante de l'interface
6. ⚠️ **Monitoring production** : Azure Insights (mentionné mais non implémenté, PostHog utilisé)

## Commandes Courantes Git

```bash
# Voir l'état
git status

# Commit avec co-auteur Claude
git add <fichiers>
git commit -m "Description du commit

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Push vers remote
git push origin main
```

## Références Techniques

- **Dataset** : Twitter Sentiment Analysis (Kaggle) - 1.6M tweets binaires (positif/négatif)
- **Embeddings** : GloVe 6B.100d (télécharger depuis Stanford NLP si nécessaire)
- **Framework ML** : TensorFlow/Keras + scikit-learn
- **API** : FastAPI + Pydantic
- **Serving** : uvicorn (ASGI)
- **Containerisation** : Docker + docker-compose
