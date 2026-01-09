# Guide d'Utilisation de l'Interface Streamlit

Interface web interactive pour tester l'API de sentiment analysis Air Paradis.

---

## 🚀 Démarrage Rapide

### 1. Installer les dépendances

```bash
cd api
pip install -r requirements-streamlit.txt
```

### 2. Lancer l'API (terminal 1)

```bash
# Avec uvicorn (FastAPI)
uvicorn app:app --reload --port 8000

# Ou avec Python
python app.py
```

L'API sera disponible sur `http://localhost:8000`

### 3. Lancer Streamlit (terminal 2)

```bash
streamlit run streamlit_app.py
```

L'interface s'ouvrira automatiquement sur `http://localhost:8501`

---

## 📋 Fonctionnalités

### Mode 1 : Tweet Unique

**Analyser un seul tweet à la fois**

1. Entrer le texte du tweet (max 280 caractères)
2. Cliquer sur **"🔍 Analyser le sentiment"**
3. Voir le résultat avec :
   - Sentiment prédit (Positif/Négatif)
   - Niveau de confiance
   - Graphique des probabilités
4. **Valider la prédiction** :
   - ✅ Cliquer sur **"Prédiction correcte"** si bon
   - ❌ Cliquer sur **"Prédiction incorrecte"** si erreur
   - Si incorrecte, indiquer le vrai sentiment
   - La trace est envoyée à Azure Application Insights

**Exemple de tweets à tester** :

```
Positif : "Amazing flight! Best crew ever, comfortable seats!"
Négatif : "Terrible experience. Flight delayed 5 hours, no apology."
Neutre : "The flight was okay, nothing special."
Ambigü : "Not bad, but could be better."
```

### Mode 2 : Analyse Batch

**Analyser plusieurs tweets simultanément (jusqu'à 100)**

**Méthode 1 : Saisie manuelle**
1. Entrer les tweets (un par ligne)
2. Cliquer sur **"🔍 Analyser tous les tweets"**
3. Voir :
   - Statistiques globales (total, positifs, négatifs)
   - Distribution des sentiments (graphiques)
   - Tableau détaillé avec tous les résultats
4. Télécharger les résultats en CSV

**Méthode 2 : Import CSV**
1. Préparer un fichier CSV avec une colonne `text`
   ```csv
   text
   "Great service!"
   "Bad experience"
   "Average flight"
   ```
2. Uploader le fichier
3. Analyser automatiquement
4. Télécharger les résultats enrichis

### Mode 3 : Historique

Visualisation des tendances de sentiment au fil du temps (en développement).

---

## ⚙️ Configuration

### Variables d'Environnement

**Option 1 : Fichier .env**

Créer un fichier `.env` dans le dossier `api/` :

```env
# URL de l'API
API_URL=http://localhost:8000

# Azure Application Insights (optionnel)
APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;IngestionEndpoint=https://...
```

**Option 2 : Streamlit Secrets (pour déploiement Streamlit Cloud)**

Créer `.streamlit/secrets.toml` :

```toml
API_URL = "https://airparadis-sentiment-api.azurewebsites.net"
APPINSIGHTS_CONNECTION_STRING = "InstrumentationKey=xxx;..."
```

### Modifier l'URL de l'API

Dans la sidebar de l'interface, vous pouvez changer l'URL de l'API en temps réel :
- Local : `http://localhost:8000`
- Heroku : `https://airparadis-sentiment.herokuapp.com`
- Azure : `https://airparadis-sentiment-api.azurewebsites.net`

---

## 🎯 Système de Validation et Feedback

### Pourquoi valider les prédictions ?

Le système de validation permet :
- ✅ **Amélioration continue** : Les corrections alimentent le ré-entraînement
- ✅ **Détection de drift** : Identifier quand le modèle devient moins précis
- ✅ **Nouveaux patterns** : Découvrir de nouveaux mots/expressions

### Comment ça marche ?

```
1. Utilisateur teste un tweet
         ↓
2. Modèle prédit le sentiment
         ↓
3. Utilisateur valide ou corrige
         ↓
4. Si incorrect → Trace envoyée à Application Insights
         ↓
5. Équipe Data Science analyse les erreurs
         ↓
6. Ré-entraînement du modèle avec corrections
         ↓
7. Déploiement de la nouvelle version
```

### Données envoyées à Application Insights

Quand vous signalez une erreur, ces informations sont envoyées :

```json
{
  "event_type": "incorrect_prediction",
  "text": "Le texte du tweet...",
  "text_length": 142,
  "predicted_sentiment": "Positif",
  "actual_sentiment": "Négatif",
  "confidence": 0.78,
  "model_type": "logistic",
  "timestamp": "2024-01-09T10:30:00",
  "source": "streamlit_interface"
}
```

Ces traces sont :
- Marquées avec le niveau **WARNING**
- Analysables dans le portail Azure
- Utilisables pour créer des alertes
- Exportables pour ré-entraînement

---

## 🎨 Personnalisation

### Thème

Streamlit utilise le thème par défaut. Pour personnaliser, créer `.streamlit/config.toml` :

```toml
[theme]
primaryColor = "#1E88E5"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### Ajouter des graphiques

L'interface utilise Plotly. Pour ajouter un graphique :

```python
import plotly.express as px

fig = px.line(df, x='date', y='sentiment', title='Évolution')
st.plotly_chart(fig, use_container_width=True)
```

---

## 🚢 Déploiement

### Déployer sur Streamlit Cloud (gratuit)

1. Push le code sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre compte GitHub
4. Sélectionner le repo et le fichier `api/streamlit_app.py`
5. Ajouter les secrets dans les paramètres
6. Déployer !

L'app sera disponible sur `https://votreapp.streamlit.app`

### Déployer avec Docker

Fichier `Dockerfile.streamlit` (déjà créé) :

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements-streamlit.txt .
RUN pip install -r requirements-streamlit.txt

COPY streamlit_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501"]
```

Build et run :

```bash
docker build -f Dockerfile.streamlit -t airparadis-streamlit .
docker run -p 8501:8501 -e API_URL=http://api:8000 airparadis-streamlit
```

---

## 🐛 Troubleshooting

### L'API n'est pas accessible

**Erreur** : `❌ API inaccessible`

**Solutions** :
1. Vérifier que l'API est lancée (`uvicorn app:app`)
2. Vérifier l'URL dans la sidebar
3. Tester l'API directement : `curl http://localhost:8000/health`

### Application Insights ne fonctionne pas

**Symptôme** : Message "mode local - Application Insights non configuré"

**Solutions** :
1. Vérifier que `APPINSIGHTS_CONNECTION_STRING` est défini
2. Installer `opencensus-ext-azure` : `pip install opencensus-ext-azure`
3. Vérifier que la connection string est valide
4. Check les logs dans la console Streamlit

### Erreur lors de l'upload CSV

**Erreur** : `Le fichier doit contenir une colonne 'text'`

**Solution** :
- Vérifier que votre CSV a bien une colonne nommée `text`
- Exemple de CSV valide :
  ```csv
  text
  "Premier tweet"
  "Deuxième tweet"
  ```

### L'interface est lente

**Solutions** :
1. Réduire le nombre de tweets en batch (< 50)
2. Optimiser l'API (caching, batch processing)
3. Utiliser un modèle plus léger (LogReg au lieu de BERT)

---

## 📊 Métriques de Performance

L'interface affiche :
- **Temps d'analyse** : Durée de traitement de chaque requête
- **Confiance moyenne** : Niveau de confiance moyen du modèle
- **Distribution** : Répartition positifs/négatifs

Pour améliorer la performance :
- Utiliser le mode batch pour plusieurs tweets
- Activer le caching dans l'API
- Déployer sur des serveurs avec plus de ressources

---

## 🔒 Sécurité

### Bonnes pratiques

✅ **Ne jamais commit** :
- Fichier `.env` avec les secrets
- Connection strings Application Insights
- Clés API privées

✅ **Utiliser** :
- `.gitignore` pour exclure `.env`
- Variables d'environnement pour secrets
- Streamlit Secrets pour déploiement

✅ **Limiter** :
- Max 100 tweets par batch (déjà implémenté)
- Rate limiting sur l'API (à implémenter)
- Validation des inputs (déjà implémenté avec Pydantic)

---

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io)
- [Plotly Documentation](https://plotly.com/python/)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Application Insights](https://docs.microsoft.com/azure/azure-monitor/app/)

---

## 🎓 Pour le Projet OpenClassrooms

### Captures d'écran à inclure

1. **Interface principale** : Vue d'ensemble avec un tweet analysé
2. **Validation** : Section de feedback avec boutons
3. **Message de confirmation** : "Trace envoyée à Application Insights"
4. **Mode batch** : Graphiques de distribution
5. **CSV export** : Tableau de résultats téléchargé

### Démonstration

Pour la soutenance, préparer :
1. Un tweet positif évident → Valider correct
2. Un tweet négatif évident → Valider correct
3. Un tweet ambigu → Corriger et montrer l'envoi à App Insights
4. Un batch de 5-10 tweets → Montrer les statistiques
5. Export CSV → Ouvrir dans Excel

---

**Bon test ! 🚀**
