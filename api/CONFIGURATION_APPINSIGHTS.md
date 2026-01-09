# Configuration Azure Application Insights

Ce guide explique comment configurer Azure Application Insights pour le monitoring de l'API et de l'interface Streamlit.

---

## 1. Créer une ressource Application Insights

### Via le portail Azure

1. Se connecter au [portail Azure](https://portal.azure.com)
2. Cliquer sur **"Créer une ressource"**
3. Rechercher **"Application Insights"**
4. Remplir les informations :
   - **Nom** : `airparadis-sentiment-insights`
   - **Région** : France Central (ou la même que votre API)
   - **Resource Group** : Utiliser le même que votre Web App
5. Cliquer sur **"Créer"**

### Via Azure CLI

```bash
# Créer la ressource Application Insights
az monitor app-insights component create \
  --app airparadis-sentiment-insights \
  --location francecentral \
  --resource-group airparadis-rg \
  --application-type web

# Récupérer la clé d'instrumentation
az monitor app-insights component show \
  --app airparadis-sentiment-insights \
  --resource-group airparadis-rg \
  --query connectionString
```

---

## 2. Récupérer les clés de connexion

Une fois la ressource créée :

1. Aller dans la ressource Application Insights
2. Dans le menu de gauche, cliquer sur **"Propriétés"**
3. Copier les valeurs suivantes :
   - **Connection String** (recommandé)
   - **Instrumentation Key** (ancienne méthode, toujours supportée)

Exemple de Connection String :
```
InstrumentationKey=12345678-1234-1234-1234-123456789abc;IngestionEndpoint=https://francecentral-1.in.applicationinsights.azure.com/;LiveEndpoint=https://francecentral.livediagnostics.monitor.azure.com/
```

---

## 3. Configuration de l'API Flask/FastAPI

### Installer les dépendances

```bash
pip install opencensus-ext-azure
```

### Configurer les variables d'environnement

**Option 1 : Fichier .env (développement local)**

Créer un fichier `.env` dans le dossier `api/` :

```env
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://...
```

**Option 2 : Variables d'environnement système**

```bash
export APPINSIGHTS_CONNECTION_STRING="InstrumentationKey=xxx;..."
```

**Option 3 : Configuration Azure Web App (production)**

Dans le portail Azure :
1. Aller dans votre Web App
2. Menu **"Configuration"** → **"Application settings"**
3. Cliquer sur **"New application setting"**
4. Ajouter :
   - Nom : `APPINSIGHTS_CONNECTION_STRING`
   - Valeur : Votre connection string

### Code API (déjà implémenté dans app.py)

```python
from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging
import os

# Configuration du logger
logger = logging.getLogger(__name__)
connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")

if connection_string:
    logger.addHandler(AzureLogHandler(connection_string=connection_string))
    logger.setLevel(logging.INFO)

# Dans vos endpoints
@app.post("/predict")
async def predict(text: str):
    # ... prédiction ...

    # Logger les prédictions avec faible confiance
    if confidence < 0.6:
        logger.warning(
            f"Low confidence prediction",
            extra={
                'custom_dimensions': {
                    'text': text[:100],
                    'confidence': confidence,
                    'prediction': prediction
                }
            }
        )
```

---

## 4. Configuration de Streamlit

### Installer les dépendances

```bash
pip install opencensus-ext-azure
```

### Configurer les variables d'environnement

**Option 1 : Fichier .env**

Créer un fichier `.env` à la racine du projet :

```env
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://...
API_URL=http://localhost:8000
```

Charger avec python-dotenv :

```python
from dotenv import load_dotenv
load_dotenv()
```

**Option 2 : Streamlit secrets (recommandé pour Streamlit Cloud)**

Créer un fichier `.streamlit/secrets.toml` :

```toml
APPINSIGHTS_CONNECTION_STRING = "InstrumentationKey=xxx;..."
API_URL = "https://airparadis-sentiment-api.azurewebsites.net"
```

Puis dans le code :

```python
import streamlit as st
APPINSIGHTS_CONNECTION_STRING = st.secrets.get("APPINSIGHTS_CONNECTION_STRING", "")
```

---

## 5. Vérifier que ça fonctionne

### Test local

1. Lancer Streamlit :
   ```bash
   streamlit run streamlit_app.py
   ```

2. Faire une prédiction et cliquer sur **"Prédiction incorrecte"**

3. Vérifier les logs dans la console :
   ```
   INFO - Trace envoyée à Application Insights: prédiction incorrecte pour 'xxx'
   ```

### Vérifier dans Azure

1. Aller dans le portail Azure → Application Insights
2. Menu **"Logs"** (ou **"Transaction search"**)
3. Exécuter la requête suivante :

```kusto
traces
| where severityLevel >= 2  // Warning et au-dessus
| where customDimensions.event_type == "incorrect_prediction"
| project timestamp, message, customDimensions
| order by timestamp desc
| take 50
```

4. Vous devriez voir les traces de prédictions incorrectes avec toutes les informations

---

## 6. Créer des Alertes

### Alerte pour prédictions incorrectes fréquentes

1. Dans Application Insights, menu **"Alerts"** → **"New alert rule"**
2. Configurer :
   - **Condition** : Custom log search
   - **Requête** :
     ```kusto
     traces
     | where severityLevel >= 2
     | where customDimensions.event_type == "incorrect_prediction"
     | summarize count() by bin(timestamp, 5m)
     | where count_ > 10  // Plus de 10 erreurs en 5 minutes
     ```
   - **Threshold** : Greater than 0
   - **Evaluation frequency** : Every 5 minutes
3. **Action group** :
   - Email : votre.email@example.com
   - SMS (optionnel)
4. Nommer l'alerte : `High Incorrect Predictions Rate`

### Alerte pour prédictions avec faible confiance

```kusto
traces
| where severityLevel >= 1  // Info
| where customDimensions.confidence < 0.6
| summarize count() by bin(timestamp, 1h)
| where count_ > 50  // Plus de 50 prédictions avec faible confiance par heure
```

---

## 7. Dashboard de Monitoring

### Créer un dashboard personnalisé

1. Dans Application Insights, menu **"Workbooks"** → **"New"**
2. Ajouter des visualisations :

**Graphique 1 : Volume de prédictions incorrectes**
```kusto
traces
| where customDimensions.event_type == "incorrect_prediction"
| summarize count() by bin(timestamp, 1h)
| render timechart
```

**Graphique 2 : Distribution par sentiment**
```kusto
traces
| where customDimensions.event_type == "incorrect_prediction"
| summarize count() by tostring(customDimensions.predicted_sentiment)
| render piechart
```

**Graphique 3 : Taux de confiance moyen**
```kusto
traces
| where customDimensions.event_type == "incorrect_prediction"
| summarize avg(todouble(customDimensions.confidence))
| render areachart
```

3. Sauvegarder le workbook : `Sentiment Analysis - User Feedback`

---

## 8. Captures d'écran pour le livrable

Pour le projet OpenClassrooms, prendre des captures d'écran de :

1. **Configuration Application Insights** :
   - Page de propriétés avec Connection String
   - Vue d'ensemble de la ressource

2. **Traces** :
   - Liste des traces de prédictions incorrectes
   - Détail d'une trace avec custom_dimensions

3. **Alertes** :
   - Configuration d'une alerte
   - Email/SMS d'alerte reçu (simuler si besoin)

4. **Dashboard** :
   - Workbook avec graphiques de monitoring

5. **Interface Streamlit** :
   - Section de validation avec boutons
   - Message de confirmation d'envoi à Application Insights

---

## 9. Mode Debug sans Application Insights

Si vous n'avez pas configuré Application Insights (tests locaux), l'application fonctionne quand même :

- Les feedbacks sont loggés dans la console
- Message affiché : "Feedback enregistré (mode local)"
- Aucune erreur, dégradation gracieuse

---

## 10. Résumé des Variables d'Environnement

| Variable | Description | Requis | Exemple |
|----------|-------------|--------|---------|
| `APPINSIGHTS_CONNECTION_STRING` | Connection string Application Insights | Non* | `InstrumentationKey=xxx;...` |
| `APPINSIGHTS_INSTRUMENTATION_KEY` | Ancienne méthode (deprecated) | Non* | `12345678-1234-...` |
| `API_URL` | URL de l'API | Oui | `http://localhost:8000` |

*Non requis pour fonctionner en mode local, mais recommandé pour production

---

## Ressources

- [Documentation Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/app-insights-overview)
- [Opencensus Azure](https://github.com/census-instrumentation/opencensus-python/tree/master/contrib/opencensus-ext-azure)
- [Kusto Query Language (KQL)](https://docs.microsoft.com/azure/data-explorer/kusto/query/)
