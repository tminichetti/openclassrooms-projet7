# Air Paradis - Sentiment Analysis API

API de prédiction de sentiments pour la détection de bad buzz en temps réel.

## 📋 Description

Cette API permet d'analyser le sentiment (positif/négatif) de tweets pour aider Air Paradis à anticiper les problèmes de réputation et détecter le bad buzz.

**Fonctionnalités principales:**
- ✅ Prédiction de sentiment (positif/négatif)
- ✅ Support de plusieurs types de modèles (BERT, LSTM, CNN, Logistic Regression)
- ✅ Prédiction unitaire et batch
- ✅ API REST avec documentation interactive
- ✅ Monitoring et logging
- ✅ Tests unitaires complets
- ✅ CI/CD avec GitHub Actions
- ✅ Déploiement Docker
- ✅ Interface Streamlit pour tests

## 🚀 Installation

### Prérequis

- Python 3.9+
- pip
- (Optionnel) Docker

### Installation locale

1. **Cloner le dépôt:**
```bash
git clone <repository_url>
cd projet7/api
```

2. **Créer un environnement virtuel:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances:**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement:**
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

5. **Lancer l'API:**
```bash
python app.py
# ou
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

L'API sera accessible à: http://localhost:8000

## 🐳 Installation avec Docker

### Docker simple

```bash
# Build
docker build -t airparadis-api .

# Run
docker run -p 8000:8000 \
  -e MODEL_TYPE=bert \
  -v $(pwd)/../models:/app/models \
  airparadis-api
```

### Docker Compose (recommandé)

```bash
# Lancer tous les services (API + Streamlit + MLFlow)
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

Services disponibles:
- API: http://localhost:8000
- Streamlit: http://localhost:8501
- MLFlow: http://localhost:5001

## 📚 Documentation

### Documentation interactive

Une fois l'API lancée, accédez à:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints principaux

#### 1. Health Check
```bash
GET /health
```

**Réponse:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_type": "bert",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 2. Prédiction simple
```bash
POST /predict
Content-Type: application/json

{
  "text": "This flight was amazing! Best experience ever!"
}
```

**Réponse:**
```json
{
  "text": "This flight was amazing! Best experience ever!",
  "sentiment": "1",
  "sentiment_label": "Positif",
  "confidence": 0.92,
  "probabilities": {
    "negative": 0.08,
    "positive": 0.92
  },
  "timestamp": "2024-01-15T10:30:00",
  "model_type": "bert"
}
```

#### 3. Prédiction batch
```bash
POST /predict/batch
Content-Type: application/json

{
  "tweets": [
    "Great service!",
    "Terrible experience",
    "Amazing quality!"
  ]
}
```

**Réponse:**
```json
{
  "predictions": [...],
  "count": 3,
  "model_type": "bert",
  "timestamp": "2024-01-15T10:30:00"
}
```

#### 4. Informations sur les modèles
```bash
GET /models
```

### Exemples avec curl

```bash
# Health check
curl http://localhost:8000/health

# Prédiction simple
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great flight experience!"}'

# Prédiction batch
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '{"tweets": ["Great!", "Bad!", "Okay"]}'
```

### Exemples avec Python

```python
import requests

# Prédiction simple
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "This is amazing!"}
)
result = response.json()
print(f"Sentiment: {result['sentiment_label']}")
print(f"Confiance: {result['confidence']:.1%}")

# Prédiction batch
response = requests.post(
    "http://localhost:8000/predict/batch",
    json={"tweets": ["Great!", "Bad!", "Okay"]}
)
results = response.json()
print(f"Analysé {results['count']} tweets")
```

## 🧪 Tests

### Exécuter les tests

```bash
# Tests simples
pytest test_api.py -v

# Tests avec couverture
pytest test_api.py -v --cov=app --cov-report=html

# Tests spécifiques
pytest test_api.py::TestPredictEndpoint -v
```

### Rapport de couverture

Après avoir exécuté les tests avec couverture, ouvrez `htmlcov/index.html` dans votre navigateur.

## 🎨 Interface Streamlit

### Lancer l'interface

```bash
streamlit run streamlit_app.py
```

Accédez à: http://localhost:8501

**Fonctionnalités:**
- Analyse de tweets unitaires
- Analyse batch (fichier CSV ou texte)
- Visualisations interactives
- Export des résultats

## 📊 Monitoring avec MLFlow

### Lancer MLFlow

```bash
mlflow ui --port 5001
```

Accédez à: http://localhost:5001

Vous pourrez voir:
- Toutes les expériences d'entraînement
- Métriques (accuracy, F1, etc.)
- Paramètres des modèles
- Artefacts sauvegardés

## 🔧 Configuration

### Variables d'environnement

Créez un fichier `.env` basé sur `.env.example`:

```bash
MODEL_TYPE=bert           # Type de modèle (bert, lstm, cnn, logistic)
MODEL_PATH=../models/...  # Chemin vers le modèle
PORT=8000                 # Port de l'API
WORKERS=2                 # Nombre de workers
```

### Changer de modèle

Pour utiliser un modèle différent:

```bash
# Via variable d'environnement
export MODEL_TYPE=lstm
export MODEL_PATH=../models/lstm_model.h5

# Via Docker
docker run -e MODEL_TYPE=bert -e MODEL_PATH=/app/models/bert airparadis-api
```

## 🚢 Déploiement

### Heroku

```bash
# Login
heroku login

# Créer l'application
heroku create airparadis-api

# Configurer les variables
heroku config:set MODEL_TYPE=bert

# Déployer
git push heroku main
```

### Azure

```bash
# Login Azure
az login

# Créer le groupe de ressources
az group create --name airparadis-rg --location westeurope

# Déployer le container
az container create \
  --resource-group airparadis-rg \
  --name airparadis-api \
  --image <your-docker-image> \
  --ports 8000 \
  --environment-variables MODEL_TYPE=bert
```

### GitHub Actions (CI/CD)

Le pipeline CI/CD est configuré dans `.github/workflows/ci-cd.yml`.

**Déclencheurs:**
- Push sur main/master
- Pull requests
- Workflow manuel

**Étapes:**
1. Tests et linting
2. Build Docker image
3. Scan de sécurité
4. Déploiement Heroku/Azure
5. Tests de smoke

**Secrets requis:**
- `HEROKU_API_KEY`
- `HEROKU_APP_NAME`
- `HEROKU_EMAIL`
- `AZURE_CREDENTIALS` (optionnel)

## 📈 Performance

### Latence

- Prédiction simple: ~100-300ms (BERT), ~10-50ms (Logistic)
- Prédiction batch (10 tweets): ~500-1000ms (BERT)

### Limites

- Texte maximum: 280 caractères
- Batch maximum: 100 tweets
- Rate limit: 100 requêtes/minute (configurable)

## 🛡️ Sécurité

- ✅ Validation des entrées avec Pydantic
- ✅ Sanitization des données
- ✅ CORS configuré
- ✅ Scan de sécurité automatique (Trivy, Safety)
- ✅ Container non-root
- ✅ Health checks

## 🤝 Contribution

### Développement

```bash
# Installer les dépendances de dev
pip install -r requirements-dev.txt

# Formatter le code
black app.py

# Linter
flake8 app.py
pylint app.py

# Tests
pytest -v
```

### Pre-commit hooks

```bash
pre-commit install
```

## 📝 TODO

- [ ] Ajouter l'authentification (JWT)
- [ ] Implémenter le rate limiting
- [ ] Ajouter le caching Redis
- [ ] Améliorer le monitoring
- [ ] Créer des dashboards Azure Insights

## 📄 Licence

Ce projet est développé dans le cadre du Projet 7 d'OpenClassrooms.

## 👤 Auteur

**Thomas** - OpenClassrooms Data Science Master

## 🙏 Remerciements

- OpenClassrooms
- Air Paradis (client fictif)
- Hugging Face (modèles BERT)
- FastAPI, Streamlit, MLFlow

## 📞 Contact

Pour toute question:
- GitHub Issues: [Créer une issue](https://github.com/...)
- Email: contact@example.com

---

Made with ❤️ for OpenClassrooms Projet 7
