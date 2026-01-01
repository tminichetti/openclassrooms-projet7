# Guide de déploiement Heroku - Air Paradis API

## Prérequis

1. Compte Heroku gratuit : https://signup.heroku.com/
2. Repository GitHub avec le code
3. Compte GitHub Student (optionnel pour avantages gratuits)

## Étapes de déploiement via GitHub

### 1. Créer l'application Heroku

1. Aller sur https://dashboard.heroku.com/
2. Cliquer sur **"New"** > **"Create new app"**
3. Nommer l'application (ex: `airparadis-sentiment-api`)
4. Choisir la région **Europe**
5. Cliquer sur **"Create app"**

### 2. Connecter GitHub

1. Dans l'onglet **"Deploy"** de votre app Heroku
2. Section **"Deployment method"** : choisir **GitHub**
3. Cliquer sur **"Connect to GitHub"**
4. Autoriser Heroku à accéder à votre compte GitHub
5. Rechercher votre repository : `openclassrooms-projet7`
6. Cliquer sur **"Connect"**

### 3. Configurer le déploiement automatique

Dans l'onglet **"Deploy"** :

1. Section **"Automatic deploys"** :
   - Choisir la branche **main** (ou **master**)
   - ✅ Cocher **"Wait for CI to pass before deploy"** (optionnel)
   - Cliquer sur **"Enable Automatic Deploys"**

2. Section **"Manual deploy"** :
   - Sélectionner la branche **main**
   - Cliquer sur **"Deploy Branch"** pour le premier déploiement

### 4. Configurer les variables d'environnement

Dans l'onglet **"Settings"** :

1. Cliquer sur **"Reveal Config Vars"**
2. Ajouter les variables suivantes :

| KEY | VALUE |
|-----|-------|
| `MODEL_TYPE` | `logistic` |
| `MODEL_PATH` | `./models/logistic_regression_model.pkl` |
| `PORT` | `8000` (automatique par Heroku) |

### 5. Configurer le buildpack (si nécessaire)

Dans l'onglet **"Settings"** > **"Buildpacks"** :

1. Cliquer sur **"Add buildpack"**
2. Sélectionner **"heroku/python"**
3. Cliquer sur **"Save changes"**

### 6. Déployer

Si vous n'avez pas activé le déploiement automatique :

1. Onglet **"Deploy"**
2. Section **"Manual deploy"**
3. Cliquer sur **"Deploy Branch"**

Le build prend environ 3-5 minutes.

### 7. Vérifier le déploiement

Une fois le build terminé :

1. Cliquer sur **"Open app"** (bouton en haut à droite)
2. Ou aller sur : `https://votre-app.herokuapp.com`

Endpoints à tester :

```bash
# Health check
https://votre-app.herokuapp.com/health

# Documentation interactive
https://votre-app.herokuapp.com/docs

# Prédiction (via l'interface Swagger)
https://votre-app.herokuapp.com/docs#/default/predict_sentiment_predict_post
```

### 8. Tester l'API

Avec curl :

```bash
# Health check
curl https://votre-app.herokuapp.com/health

# Prédiction
curl -X POST "https://votre-app.herokuapp.com/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Great flight experience!"}'
```

Avec Python :

```python
import requests

API_URL = "https://votre-app.herokuapp.com"

# Test health
response = requests.get(f"{API_URL}/health")
print(response.json())

# Test prédiction
response = requests.post(
    f"{API_URL}/predict",
    json={"text": "Amazing service!"}
)
print(response.json())
```

## Monitoring et Logs

### Voir les logs en temps réel

1. Dans le dashboard Heroku, onglet **"More"** > **"View logs"**

Ou via CLI :

```bash
heroku logs --tail --app votre-app
```

### Métriques

Dans l'onglet **"Metrics"** vous pouvez voir :
- Temps de réponse
- Utilisation mémoire
- Nombre de requêtes
- Erreurs

## Troubleshooting

### L'application crash au démarrage

1. Vérifier les logs : **More** > **View logs**
2. Vérifier que `Procfile` est correct
3. Vérifier que `requirements.txt` contient toutes les dépendances
4. Vérifier que les variables d'environnement sont définies

### L'application est lente

1. Le plan gratuit Heroku a des limitations de RAM (512 MB)
2. Le modèle logistique est plus rapide que BERT
3. L'application se met en veille après 30 min d'inactivité (premier accès lent)

### Erreur "slug size too large"

1. Vérifier que les gros modèles ne sont pas dans Git
2. Utiliser `.slugignore` pour exclure les fichiers inutiles
3. Le modèle logistique est suffisamment petit (~450 KB)

### Modèle non trouvé

1. Vérifier que les modèles sont bien dans le dossier `api/models/`
2. Vérifier que le `.gitignore` autorise bien les fichiers `.pkl` légers
3. Vérifier la variable d'environnement `MODEL_PATH`

## CI/CD avec GitHub Actions (Optionnel)

Pour automatiser les tests avant le déploiement, créer `.github/workflows/deploy.yml` :

```yaml
name: Deploy to Heroku

on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd api
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd api
          pytest test_api.py -v
```

## Limites du plan gratuit Heroku

- ⚠️ **550-1000 heures gratuites par mois** (avec vérification carte bancaire)
- ⚠️ **Mise en veille après 30 min d'inactivité**
- ⚠️ **512 MB RAM max**
- ⚠️ **Slug size 500 MB max**
- ✅ **SSL gratuit**
- ✅ **Domaine personnalisé gratuit**

## Alternatives gratuites

Si Heroku ne fonctionne pas :

1. **Railway.app** (500h gratuites/mois)
2. **Render.com** (750h gratuites/mois)
3. **Fly.io** (plan gratuit généreux)
4. **Azure App Service** (F1 gratuit avec compte étudiant)

## Support

Pour toute question :
- Documentation Heroku : https://devcenter.heroku.com/
- Documentation API : https://votre-app.herokuapp.com/docs
