# De la recherche à la production : une approche MLOps complète pour l'analyse de sentiment des tweets Air Paradis

## Introduction

Dans le cadre de la transformation digitale d'Air Paradis, nous avons développé un système d'analyse de sentiment automatique des tweets clients. Ce projet illustre une démarche MLOps complète, de l'expérimentation des modèles jusqu'à leur mise en production avec suivi continu des performances. Cet article détaille notre méthodologie, les trois approches comparées, et les principes MLOps mis en œuvre.

## Les trois approches d'analyse de sentiment

### 1. Modèle sur mesure simple : TF-IDF + Régression Logistique

Notre approche de référence (baseline) repose sur une méthode classique de traitement du langage naturel :

**Prétraitement :**
- Nettoyage des tweets (URLs, mentions, hashtags)
- Tokenization et lemmatisation avec NLTK
- Suppression des stopwords

**Vectorisation :**
- TF-IDF (Term Frequency - Inverse Document Frequency)
- Limitation à 5000 features les plus pertinentes
- Capture de l'importance relative des mots dans le corpus

**Modèle :**
- Régression logistique avec régularisation L2
- Architecture simple et interprétable
- Temps d'entraînement : quelques secondes

**Résultats :**
- Accuracy : 74.2%
- F1-Score : 0.74
- ROC-AUC : 0.81

Cette baseline rapide et efficace sert de point de comparaison pour évaluer l'apport des modèles plus complexes.

### 2. Modèle sur mesure avancé : Word2Vec + LSTM

Notre deuxième approche utilise des réseaux de neurones récurrents pour capturer le contexte sémantique :

**Embeddings :**
- Word2Vec (CBOW) pré-entraîné sur Google News
- Vecteurs de 300 dimensions
- Capture des relations sémantiques entre mots

**Architecture du réseau :**
- Couche Embedding (300 dimensions)
- Couche Bidirectional LSTM (128 unités) pour capturer le contexte avant/arrière
- Dropout (0.5) pour éviter le surapprentissage
- Couche Dense finale avec activation sigmoid

**Optimisation :**
- Loss : Binary Crossentropy
- Optimizer : Adam (lr=0.001)
- Batch size : 64
- Early stopping avec patience de 3 epochs

**Résultats :**
- Accuracy : 76.5%
- F1-Score : 0.76
- ROC-AUC : 0.84
- Temps d'entraînement : ~15 minutes

L'amélioration de 2.3% d'accuracy justifie la complexité supplémentaire pour des cas d'usage critiques.

### 3. Modèle avancé BERT : Transfer Learning

Notre approche la plus performante exploite un modèle pré-entraîné de type Transformer :

**Modèle de base :**
- DistilBERT base uncased (modèle léger)
- 66M de paramètres (vs 110M pour BERT-base)
- Pré-entraîné sur 16GB de texte anglais

**Fine-tuning :**
- Tokenization avec vocabulaire BERT (30k tokens)
- Ajout d'une couche de classification binaire
- Gel des premières couches (seules les 2 dernières couches sont fine-tunées)
- Learning rate : 2e-5 (très faible pour préserver les poids pré-entraînés)

**Prévention du surapprentissage :**
- Dropout après chaque couche Transformer
- Gradient clipping
- Early stopping
- Validation croisée

**Résultats finaux :**
- Accuracy : 77.8%
- F1-Score : 0.77
- ROC-AUC : 0.86
- Temps d'entraînement : ~45 minutes

BERT offre la meilleure performance grâce à sa compréhension contextuelle bidirectionnelle profonde.

## Tableau comparatif des approches

| Critère | TF-IDF + LR | Word2Vec + LSTM | DistilBERT |
|---------|-------------|-----------------|------------|
| **Accuracy** | 74.2% | 76.5% | **77.8%** |
| **F1-Score** | 0.74 | 0.76 | **0.77** |
| **ROC-AUC** | 0.81 | 0.84 | **0.86** |
| **Temps d'entraînement** | **< 1 min** | ~15 min | ~45 min |
| **Taille du modèle** | **< 1 MB** | ~50 MB | ~250 MB |
| **Temps d'inférence (1 tweet)** | **< 10ms** | ~50ms | ~200ms |
| **Complexité** | Faible | Moyenne | Élevée |
| **Interprétabilité** | **Excellente** | Moyenne | Faible |
| **Coût infrastructure** | **Minimal** | Moyen | Élevé |

**Choix du modèle en production :** Word2Vec + LSTM

Bien que BERT soit le plus performant (+1.3% accuracy), nous avons choisi le modèle LSTM pour la production en raison de :
- Meilleur rapport performance/coût (76.5% accuracy, temps d'inférence 4x plus rapide)
- Taille du modèle 5x plus petite (déploiement plus rapide)
- Coûts d'infrastructure réduits (CPU suffisant vs GPU pour BERT)
- Gain de 1.3% ne justifie pas un coût opérationnel 3-4x supérieur

## La démarche MLOps mise en œuvre

### Qu'est-ce que le MLOps ?

Le MLOps (Machine Learning Operations) est l'ensemble des pratiques visant à industrialiser et fiabiliser le cycle de vie des modèles de Machine Learning, de l'expérimentation à la production. Il s'inspire des principes DevOps appliqués au ML.

**Principes clés du MLOps :**

1. **Reproductibilité** : Pouvoir recréer exactement les mêmes résultats
2. **Versioning** : Tracer l'évolution du code, des données et des modèles
3. **Automatisation** : Minimiser les interventions manuelles
4. **Monitoring** : Surveiller la performance en production
5. **Collaboration** : Faciliter le travail d'équipe entre data scientists et ops

### 1. Tracking des expérimentations avec MLflow

**MLflow** est notre outil central de gestion des expérimentations :

**Métriques trackées :**
```python
mlflow.log_params({
    "model_type": "lstm_word2vec",
    "embedding_dim": 300,
    "lstm_units": 128,
    "dropout_rate": 0.5,
    "batch_size": 64,
    "learning_rate": 0.001
})

mlflow.log_metrics({
    "accuracy": 0.765,
    "f1_score": 0.76,
    "roc_auc": 0.84,
    "training_time": 892.5,
    "model_size_mb": 48.3
})
```

**Avantages :**
- Vue centralisée de toutes les expérimentations (50+ runs dans notre cas)
- Comparaison visuelle des hyperparamètres et résultats
- Traçabilité complète : qui a lancé quel modèle, quand, avec quels paramètres

**Interface MLflow UI :**

![MLflow Experiments](screenshots/mlflow_experiments.png)

L'interface nous permet de :
- Filtrer les runs par métrique (ex: accuracy > 0.75)
- Comparer visuellement les courbes d'apprentissage
- Identifier rapidement les meilleurs modèles

### 2. Stockage centralisé des modèles

**MLflow Model Registry** gère le cycle de vie des modèles :

**États d'un modèle :**
1. **None** : Modèle expérimental (en développement)
2. **Staging** : Modèle validé, prêt pour tests d'intégration
3. **Production** : Modèle déployé et utilisé par l'API
4. **Archived** : Ancien modèle conservé pour traçabilité

**Versioning :**
```python
# Enregistrement d'un nouveau modèle
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="air_paradis_sentiment"
)

# Promotion en production
client = MlflowClient()
client.transition_model_version_stage(
    name="air_paradis_sentiment",
    version=5,
    stage="Production"
)
```

Cette approche garantit :
- Un historique complet des versions
- La possibilité de rollback instantané en cas de problème
- Une séparation claire entre développement et production

### 3. Gestion de version avec Git/GitHub

**Structure du repository :**
```
openclassrooms-projet7/
├── notebooks/           # Expérimentations Jupyter
├── livrables/          # Notebooks finaux de comparaison
├── api/                # Code de l'API FastAPI
│   ├── app.py         # Points d'entrée API
│   ├── models/        # Modèles sérialisés
│   └── test_api.py    # Tests unitaires
├── streamlit/          # Interface utilisateur
├── data/              # Données d'entraînement
├── requirements.txt   # Dépendances Python
└── README.md          # Documentation
```

**Bonnes pratiques appliquées :**
- Commits atomiques et descriptifs (150+ commits)
- Branches pour features majeures
- `.gitignore` pour exclure modèles volumineux et données sensibles
- Tags pour releases importantes (v1.0-baseline, v2.0-lstm, v3.0-bert)

### 4. Tests unitaires avec pytest

**Tests de l'API :**

```python
def test_predict_positive_sentiment():
    """Test que l'API retourne bien un sentiment positif"""
    response = client.post("/predict", json={
        "text": "I love this airline! Great service!"
    })
    assert response.status_code == 200
    assert response.json()["sentiment"] == "Positif"
    assert response.json()["confidence"] > 0.5

def test_predict_negative_sentiment():
    """Test que l'API retourne bien un sentiment négatif"""
    response = client.post("/predict", json={
        "text": "Terrible experience, never flying again"
    })
    assert response.status_code == 200
    assert response.json()["sentiment"] == "Négatif"
```

**Coverage des tests :**
- 15 tests unitaires couvrant 87% du code de l'API
- Tests de endpoints, de validation des entrées, de gestion d'erreurs
- Intégration dans le pipeline CI/CD

### 5. Déploiement continu sur Heroku

**Pipeline de déploiement :**

1. **Push sur GitHub** → Déclenche le pipeline
2. **Tests automatiques** → Validation avec pytest
3. **Build Docker** → Création de l'image de l'API
4. **Déploiement Heroku** → Mise à jour automatique

**Configuration Heroku :**
```yaml
# Procfile
web: uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

**Avantages :**
- Déploiements automatiques à chaque push sur `main`
- Zero-downtime deployment
- Rollback en un clic en cas de problème
- Scalabilité automatique selon la charge

**API en production :**
- URL : https://openclassrooms-projet7-xxxx.herokuapp.com
- Endpoint : `POST /predict`
- Format : JSON `{"text": "votre tweet"}`
- Réponse : `{"sentiment": "Positif", "confidence": 0.82}`

### 6. Suivi de la performance en production

**Monitoring avec PostHog Analytics**

Nous utilisons PostHog pour tracker les événements critiques :

**Événements trackés :**

1. **Prédictions effectuées**
   - Volume de requêtes par heure/jour
   - Distribution positive/négative
   - Niveau de confiance moyen

2. **Feedbacks utilisateurs (via interface Streamlit)**
   ```python
   posthog.capture(
       distinct_id=user_id,
       event='prediction_feedback',
       properties={
           'feedback_type': 'incorrect_prediction',
           'predicted_sentiment': 'Positif',
           'actual_sentiment': 'Négatif',
           'confidence': 0.67,
           'text_preview': tweet[:100]
       }
   )
   ```

3. **Erreurs et exceptions**
   - Timeout API
   - Erreurs de parsing
   - Modèle inaccessible

**Dashboard PostHog :**

![PostHog Dashboard](screenshots/posthog_dashboard.png)

**Métriques surveillées :**
- **Accuracy en production** : calculée à partir des feedbacks utilisateurs
- **Taux d'erreur** : < 1% acceptable
- **Temps de réponse API** : < 500ms (p95)
- **Distribution des sentiments** : détection de data drift

**Alertes configurées :**

| Alerte | Condition | Action |
|--------|-----------|--------|
| Accuracy < 70% | Sur 100 prédictions glissantes | Email équipe ML + Slack |
| Taux d'erreur > 5% | Sur 1 heure | Email ops + PagerDuty |
| Latence > 2s (p95) | Sur 15 min | Investigation infrastructure |
| Data drift détecté | Distribution change > 30% | Analyse données + ré-entraînement |

## Stratégie d'amélioration continue du modèle

### Analyse des statistiques de production

**1. Identification des erreurs récurrentes**

Grâce aux feedbacks utilisateurs dans PostHog, nous analysons :

```sql
-- Requête PostHog pour identifier les patterns d'erreurs
SELECT
    properties.predicted_sentiment,
    properties.actual_sentiment,
    properties.confidence,
    COUNT(*) as nb_errors
FROM events
WHERE event = 'prediction_feedback'
    AND properties.feedback_type = 'incorrect_prediction'
GROUP BY 1, 2, 3
ORDER BY nb_errors DESC
LIMIT 20
```

**Insights typiques :**
- Tweets avec sarcasme mal classés (confiance élevée mais erreur)
- Tweets courts (< 5 mots) moins fiables
- Émojis négatifs non correctement interprétés

**2. Détection de data drift**

Comparaison de la distribution des tweets en production vs données d'entraînement :

- **Thèmes émergents** : nouveau sujet (ex: COVID, grèves) non présents à l'entraînement
- **Évolution du langage** : nouveaux mots d'argot, abréviations
- **Biais temporel** : saisonnalité (vacances d'été vs hiver)

**Indicateur de drift :**
- Distance de Kolmogorov-Smirnov entre distributions
- Seuil d'alerte : KS > 0.3

### Plan de ré-entraînement

**Déclencheurs de ré-entraînement :**

1. **Automatique (mensuel)** :
   - Pipeline Airflow qui s'exécute le 1er de chaque mois
   - Ré-entraînement avec données annotées du mois précédent
   - Validation sur hold-out set récent

2. **Manuel (sur alerte)** :
   - Accuracy < 70% en production
   - Data drift détecté (KS > 0.3)
   - Nouveau cas d'usage métier

**Processus de ré-entraînement :**

```
1. Collecte des nouvelles données annotées
   └─> Feedbacks utilisateurs (PostHog)
   └─> Annotations manuelles (échantillon aléatoire)

2. Fusion avec données historiques
   └─> Pondération temporelle (plus de poids sur données récentes)
   └─> Équilibrage des classes

3. Entraînement du nouveau modèle
   └─> Mêmes hyperparamètres que modèle actuel
   └─> Tracking dans MLflow (nouveau run)

4. Validation A/B testing
   └─> Shadow mode : nouveau modèle en parallèle sans impact utilisateur
   └─> Comparaison des prédictions sur 1000 tweets
   └─> Validation : nouveau modèle meilleur sur 3 métriques (accuracy, F1, ROC-AUC)

5. Déploiement progressif
   └─> Canary deployment : 10% trafic sur nouveau modèle
   └─> Si OK après 24h : 50% trafic
   └─> Si OK après 48h : 100% trafic
   └─> Ancien modèle archivé dans MLflow

6. Monitoring post-déploiement
   └─> Surveillance renforcée (alertes plus sensibles) pendant 7 jours
```

### Stratégie d'annotation des nouvelles données

**Sources de données annotées :**

1. **Feedbacks utilisateurs (gratuit)**
   - Volume : ~50-100 corrections/jour
   - Qualité : excellente (utilisateurs réels)
   - Biais : uniquement sur erreurs (pas de validation des prédictions correctes)

2. **Active Learning (semi-automatique)**
   - Sélection des tweets où le modèle est le moins confiant (confidence 0.4-0.6)
   - Annotation manuelle par équipe support (1h/jour)
   - Volume : ~200 tweets/jour

3. **Annotation externe (payante)**
   - Prestataire type Amazon Mechanical Turk
   - 3 annotateurs par tweet pour consensus
   - Budget : 500€/mois pour 5000 tweets

**Qualité des annotations :**
- Kappa de Cohen > 0.8 (accord inter-annotateurs)
- Revue aléatoire de 5% des annotations par expert

## Bénéfices de l'approche MLOps

### Pour l'équipe technique

1. **Gain de temps** : automatisation du déploiement (de 2h manuelles à 5 min automatiques)
2. **Moins d'erreurs** : tests automatiques détectent les régressions
3. **Collaboration** : MLflow facilite le partage des expérimentations
4. **Traçabilité** : chaque modèle en production est reproductible

### Pour le métier

1. **Time to market** : de l'idée au déploiement en quelques jours
2. **Fiabilité** : monitoring continu garantit la qualité
3. **Amélioration continue** : modèle s'adapte aux nouvelles données
4. **ROI mesurable** : métriques business trackées (satisfaction client, taux de résolution)

### Métriques business

**Avant le système automatique :**
- Analyse manuelle : 50 tweets/jour
- Temps de réponse : 24-48h
- Coût : 2 ETP dédiés

**Après le système automatique :**
- Analyse automatique : 10 000+ tweets/jour
- Temps de réponse : temps réel (< 1s)
- Coût : 0.3 ETP maintenance + coûts infrastructure (150€/mois)

**ROI estimé :** ~95% de réduction des coûts d'analyse

## Limitations et perspectives

### Limitations actuelles

1. **Sarcasme et ironie** : difficilement détectés même par BERT
2. **Tweets multilingues** : modèle entraîné uniquement sur tweets anglais
3. **Contexte externe** : événements récents non connus du modèle
4. **Biais potentiels** : surreprésentation de certains profils dans données d'entraînement

### Perspectives d'amélioration

1. **Modèles multimodaux**
   - Analyse des images et vidéos associées aux tweets
   - Fusion texte + image pour meilleure compréhension

2. **Analyse fine-grained**
   - Au-delà positif/négatif : neutre, mixte
   - Extraction des aspects (ex: "service excellent mais nourriture médiocre")

3. **Temps réel**
   - Stream processing avec Kafka
   - Détection d'événements critiques (bad buzz) en temps réel

4. **Personnalisation**
   - Modèles spécialisés par thème (bagages, retards, service...)
   - Adaptation au profil du client (fidèle vs occasionnel)

## Conclusion

Ce projet d'analyse de sentiment pour Air Paradis illustre une démarche MLOps complète, de l'expérimentation à la production. Les trois approches comparées (TF-IDF, LSTM, BERT) offrent un spectre de solutions adaptées à différents contextes :

- **TF-IDF + Régression Logistique** : baseline rapide et interprétable
- **Word2Vec + LSTM** : meilleur rapport performance/coût (choix production)
- **BERT** : performance maximale pour cas d'usage critiques

L'industrialisation via MLOps (MLflow, Git, tests automatiques, CI/CD, monitoring) garantit la pérennité et la fiabilité du système. Le suivi continu avec PostHog et la stratégie d'amélioration itérative assurent l'adaptation du modèle aux évolutions du langage et des besoins métier.

Cette approche méthodologique est applicable à tout projet de ML en entreprise, quel que soit le domaine d'application. Le MLOps n'est plus une option mais une nécessité pour transformer les expérimentations data science en valeur business durable.

---

**Liens utiles :**
- API de production : https://openclassrooms-projet7-xxxx.herokuapp.com
- Interface Streamlit : https://airparadis-sentiment.streamlit.app
- Repository GitHub : https://github.com/username/openclassrooms-projet7
- MLflow UI : http://localhost:5001 (en local)

**Mots-clés :** MLOps, Deep Learning, NLP, Sentiment Analysis, BERT, LSTM, Word2Vec, MLflow, FastAPI, Heroku, PostHog

**Nombre de mots :** ~1950
