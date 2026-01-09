# Changelog - Ajout du Système de Validation avec Application Insights

Date: 2026-01-09

---

## 🎯 Objectif

Ajouter un système de validation utilisateur dans l'interface Streamlit pour permettre aux utilisateurs de corriger les prédictions incorrectes et envoyer des traces à Azure Application Insights.

**Conformité au livrable OpenClassrooms** :
> "Une interface de test de l'API (notebook ou application Streamlit), exécutée en local, qui permet la saisie d'un tweet, affiche la prédiction, **demande une validation à l'utilisateur de la pertinence de la prédiction**, et **envoie une trace au service Application Insight en cas de non validation**"

---

## 📝 Modifications Apportées

### 1. Fichier `streamlit_app.py`

#### Imports ajoutés
```python
import logging

# Configuration du logging pour Application Insights
logging.basicConfig(level=logging.INFO)
```

#### Configuration Application Insights (lignes 36-61)
```python
# Configuration Azure Application Insights (optionnel)
APPINSIGHTS_INSTRUMENTATION_KEY = os.getenv("APPINSIGHTS_INSTRUMENTATION_KEY", "")
APPINSIGHTS_CONNECTION_STRING = os.getenv("APPINSIGHTS_CONNECTION_STRING", "")

# Flag pour activer/désactiver Application Insights
USE_APP_INSIGHTS = bool(APPINSIGHTS_CONNECTION_STRING or APPINSIGHTS_INSTRUMENTATION_KEY)

# Importer Application Insights si disponible
if USE_APP_INSIGHTS:
    try:
        from opencensus.ext.azure.log_exporter import AzureLogHandler
        logger = logging.getLogger(__name__)

        if APPINSIGHTS_CONNECTION_STRING:
            logger.addHandler(AzureLogHandler(connection_string=APPINSIGHTS_CONNECTION_STRING))
        elif APPINSIGHTS_INSTRUMENTATION_KEY:
            logger.addHandler(AzureLogHandler(instrumentation_key=APPINSIGHTS_INSTRUMENTATION_KEY))

        logger.info("Application Insights configuré avec succès")
    except ImportError:
        USE_APP_INSIGHTS = False
        logger = logging.getLogger(__name__)
        logger.warning("opencensus-ext-azure non installé.")
else:
    logger = logging.getLogger(__name__)
    logger.info("Application Insights non configuré")
```

#### Nouvelle fonction `send_feedback_to_appinsights` (lignes 174-211)

Fonction qui envoie les feedbacks utilisateurs à Application Insights avec toutes les métadonnées nécessaires :

```python
def send_feedback_to_appinsights(text, predicted_sentiment, actual_sentiment, confidence, model_type):
    """
    Envoie un feedback utilisateur à Azure Application Insights

    Args:
        text: Le texte du tweet
        predicted_sentiment: Sentiment prédit par le modèle
        actual_sentiment: Sentiment réel indiqué par l'utilisateur
        confidence: Niveau de confiance de la prédiction
        model_type: Type de modèle utilisé
    """
    if USE_APP_INSIGHTS:
        try:
            logger.warning(
                f"Prédiction incorrecte détectée par l'utilisateur",
                extra={
                    'custom_dimensions': {
                        'event_type': 'incorrect_prediction',
                        'text': text[:100],
                        'text_length': len(text),
                        'predicted_sentiment': predicted_sentiment,
                        'actual_sentiment': actual_sentiment,
                        'confidence': confidence,
                        'model_type': model_type,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'streamlit_interface'
                    }
                }
            )
            logger.info(f"Trace envoyée à Application Insights")
            return True
        except Exception as e:
            logger.error(f"Erreur lors de l'envoi: {e}")
            return False
    else:
        # Mode debug local
        logger.info(f"[LOCAL DEBUG] Prédiction incorrecte: {text[:50]}...")
        return False
```

#### Section de validation ajoutée (après le graphique, lignes 335-423)

Interface utilisateur pour valider/corriger les prédictions :

1. **Boutons de validation** :
   - "✅ Prédiction correcte"
   - "❌ Prédiction incorrecte"

2. **Si incorrecte, demander le vrai sentiment** :
   - "😊 En réalité, c'était POSITIF"
   - "😞 En réalité, c'était NÉGATIF"

3. **Envoi automatique à Application Insights** avec message de confirmation

4. **Section explicative** (expandable) qui explique comment fonctionne le système

---

### 2. Fichier `requirements-streamlit.txt`

Ajout de la dépendance Application Insights :

```txt
# Azure Application Insights (optionnel - pour monitoring)
opencensus-ext-azure==1.1.9
```

---

### 3. Nouveau fichier `CONFIGURATION_APPINSIGHTS.md`

Guide complet de configuration d'Azure Application Insights :

- Création de la ressource Azure
- Récupération des clés
- Configuration de l'API
- Configuration de Streamlit
- Vérification du fonctionnement
- Création d'alertes
- Création de dashboards
- Requêtes KQL (Kusto Query Language)

---

### 4. Nouveau fichier `STREAMLIT_GUIDE.md`

Guide d'utilisation complet de l'interface Streamlit :

- Installation et démarrage
- Utilisation de chaque mode
- Configuration
- Système de validation et feedback
- Personnalisation
- Déploiement
- Troubleshooting
- Conseils pour la soutenance

---

### 5. Nouveau fichier `test_streamlit_feedback.py`

Script de test standalone pour vérifier la configuration :

- Vérifie la présence des variables d'environnement
- Teste l'import d'opencensus-ext-azure
- Envoie 3 feedbacks de test à Application Insights
- Affiche les instructions pour vérifier dans Azure

Usage :
```bash
python test_streamlit_feedback.py
```

---

## 🎨 Aperçu de l'Interface

### Avant (ce qui existait)
```
[Zone de texte pour le tweet]
[Bouton "Analyser"]
[Résultat affiché: Sentiment + Confiance]
[Graphique des probabilités]
[JSON brut]
```

### Après (nouveau)
```
[Zone de texte pour le tweet]
[Bouton "Analyser"]
[Résultat affiché: Sentiment + Confiance]
[Graphique des probabilités]
[JSON brut]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Validation de la prédiction
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Votre feedback nous aide à améliorer le modèle

[✅ Prédiction correcte]  [❌ Prédiction incorrecte]

→ Si incorrecte:
  ⚠️ Quelle était la bonne réponse ?
  [😊 En réalité, c'était POSITIF]  [😞 En réalité, c'était NÉGATIF]

→ Message de confirmation:
  ✅ Merci ! Trace envoyée à Azure Application Insights

[ℹ️ Comment fonctionne le feedback ? (expandable)]
```

---

## 🚀 Utilisation

### Mode Local (sans Application Insights)

```bash
# 1. Lancer l'API
cd api
uvicorn app:app --reload --port 8000

# 2. Lancer Streamlit
streamlit run streamlit_app.py
```

Fonctionnement :
- ✅ Interface complète fonctionne
- ✅ Validation des prédictions fonctionne
- ⚠️ Pas d'envoi à Application Insights
- 📝 Logs dans la console seulement
- 💬 Message : "Feedback enregistré (mode local)"

### Mode Production (avec Application Insights)

```bash
# 1. Créer .env avec la connection string
echo 'APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...' > .env

# 2. Installer la dépendance
pip install opencensus-ext-azure

# 3. Lancer Streamlit
streamlit run streamlit_app.py
```

Fonctionnement :
- ✅ Interface complète
- ✅ Validation des prédictions
- ✅ Envoi à Application Insights
- 📊 Traces visibles dans Azure
- 💬 Message : "Trace envoyée à Azure Application Insights"

---

## 📊 Données Envoyées à Application Insights

### Structure de la trace

```json
{
  "timestamp": "2024-01-09T10:30:00Z",
  "severityLevel": 2,  // WARNING
  "message": "Prédiction incorrecte détectée par l'utilisateur",
  "customDimensions": {
    "event_type": "incorrect_prediction",
    "text": "This flight was terrible...",
    "text_length": 142,
    "predicted_sentiment": "Positif",
    "actual_sentiment": "Négatif",
    "confidence": 0.78,
    "model_type": "logistic",
    "timestamp": "2024-01-09T10:30:00",
    "source": "streamlit_interface"
  }
}
```

### Requête KQL pour analyser les feedbacks

```kusto
traces
| where severityLevel >= 2  // WARNING et au-dessus
| where customDimensions.event_type == "incorrect_prediction"
| where customDimensions.source == "streamlit_interface"
| project
    timestamp,
    text = tostring(customDimensions.text),
    predicted = tostring(customDimensions.predicted_sentiment),
    actual = tostring(customDimensions.actual_sentiment),
    confidence = todouble(customDimensions.confidence),
    model = tostring(customDimensions.model_type)
| order by timestamp desc
```

---

## ✅ Conformité aux Critères

### Critère CE2 - Livrable 10

> "Une interface de test de l'API (notebook ou application Streamlit), exécutée en local, qui permet la saisie d'un tweet, affiche la prédiction, demande une validation à l'utilisateur de la pertinence de la prédiction, et envoie une trace au service Application Insight en cas de non validation"

**Vérification** :
- ✅ Interface Streamlit : OUI
- ✅ Exécution en local : OUI (`streamlit run streamlit_app.py`)
- ✅ Saisie d'un tweet : OUI (zone de texte avec limite 280 caractères)
- ✅ Affiche la prédiction : OUI (sentiment + confiance + graphique)
- ✅ Demande validation : OUI (boutons "Correct" / "Incorrect")
- ✅ Envoie trace si incorrect : OUI (via opencensus-ext-azure)
- ✅ Trace à Application Insights : OUI (custom_dimensions complètes)

---

## 🎓 Pour la Soutenance

### Captures d'écran à préparer

1. **Interface principale** avec un tweet analysé
2. **Section de validation** avec les boutons visibles
3. **Correction en cours** (après clic sur "Incorrect")
4. **Message de confirmation** "Trace envoyée à Application Insights"
5. **Portail Azure** - Liste des traces reçues
6. **Détail d'une trace** dans Azure avec custom_dimensions

### Démonstration suggérée

```
1. Montrer l'interface Streamlit lancée localement
2. Taper un tweet ambigu : "Not bad, could be better"
3. Lancer l'analyse → Voir que le modèle prédit "Positif"
4. Cliquer sur "❌ Prédiction incorrecte"
5. Cliquer sur "😞 En réalité, c'était NÉGATIF"
6. Montrer le message de confirmation
7. Basculer sur le portail Azure
8. Montrer la trace reçue avec toutes les infos
9. Expliquer comment l'équipe Data Science utilise ces traces
```

---

## 🔧 Tests

### Test manuel

```bash
# 1. Lancer l'API
uvicorn app:app --reload --port 8000

# 2. Lancer Streamlit
streamlit run streamlit_app.py

# 3. Tester un tweet avec feedback incorrect
# 4. Vérifier dans les logs que la trace est envoyée
# 5. Vérifier dans Azure Portal que la trace est reçue
```

### Test automatique

```bash
# Avec Application Insights configuré
python test_streamlit_feedback.py

# Résultat attendu:
# ✅ Trace envoyée: 'This flight was amazing!...'
# ✅ Trace envoyée: 'Terrible experience....'
# ✅ Trace envoyée: 'The service was okay...'
```

---

## 📚 Fichiers Modifiés/Créés

### Modifiés
- ✏️ `api/streamlit_app.py` (+150 lignes)
- ✏️ `api/requirements-streamlit.txt` (+2 lignes)

### Créés
- ✨ `api/CONFIGURATION_APPINSIGHTS.md` (guide configuration)
- ✨ `api/STREAMLIT_GUIDE.md` (guide utilisation)
- ✨ `api/test_streamlit_feedback.py` (script de test)
- ✨ `api/CHANGELOG_STREAMLIT.md` (ce fichier)

---

## 🎯 Prochaines Étapes (Optionnel)

### Améliorations possibles

1. **Stockage local des feedbacks**
   - Enregistrer dans une base SQLite locale
   - Permettre export CSV des corrections

2. **Statistiques de feedback**
   - Tableau de bord avec taux de correction
   - Graphiques d'évolution de la précision

3. **Ré-entraînement automatique**
   - Script qui récupère les feedbacks depuis Azure
   - Ré-entraîne le modèle automatiquement
   - Déploie la nouvelle version

4. **A/B Testing**
   - Tester plusieurs modèles en parallèle
   - Comparer les taux de validation

---

**Fin du changelog**

Toutes les fonctionnalités requises par le livrable sont maintenant implémentées ! ✅
