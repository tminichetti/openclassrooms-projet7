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
- Accuracy : 78.03%
- F1-Score : 0.7810
- ROC-AUC : 0.8608

Cette baseline rapide et efficace offre d'excellentes performances et sert de point de comparaison pour évaluer l'apport des modèles plus complexes.

### 2. Modèle sur mesure avancé : Word2Vec + LSTM

Notre deuxième approche utilise des réseaux de neurones récurrents pour capturer le contexte sémantique :

**Embeddings :**
- Word2Vec (CBOW) entraîné sur nos données Twitter
- Vecteurs de 300 dimensions
- Capture des relations sémantiques spécifiques au vocabulaire des réseaux sociaux

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
- Accuracy : 77.51%
- F1-Score : 0.7777
- ROC-AUC : 0.8585
- Temps d'entraînement : ~30 minutes

Le modèle atteint de bonnes performances mais reste légèrement en-dessous de la baseline logistique.

### 3. Modèle avancé BERT : Transfer Learning

Notre approche la plus performante exploite un modèle pré-entraîné de type Transformer :

**Modèle de base :**
- BERT base uncased
- 110M de paramètres
- Pré-entraîné sur BookCorpus et Wikipedia anglais

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
- Accuracy : 77.82%
- F1-Score : 0.7707
- ROC-AUC : 0.8622
- Temps d'entraînement : ~5 heures sur GPU

BERT offre le meilleur ROC-AUC grâce à sa compréhension contextuelle bidirectionnelle profonde, mais ses performances globales sont similaires aux autres approches.

## Tableau comparatif des approches

| Critère | TF-IDF + LR | Word2Vec + BiLSTM | BERT |
|---------|-------------|-------------------|------|
| **Accuracy** | **78.03%** | 77.51% | 77.82% |
| **F1-Score** | **0.7810** | 0.7777 | 0.7707 |
| **ROC-AUC** | 0.8608 | 0.8585 | **0.8622** |
| **Temps d'entraînement** | **12 sec** | ~30 min | ~5h |
| **Taille du modèle** | **< 10 MB** | ~50 MB | ~500 MB |
| **Temps d'inférence (1 tweet)** | **< 10ms** | ~50ms | ~200ms |
| **Complexité** | **Faible** | Moyenne | Élevée |
| **Interprétabilité** | **Excellente** | Faible | Faible |
| **Coût infrastructure** | **Minimal** | Moyen | Élevé |

**Choix du modèle en production :** Régression Logistique TF-IDF

Contre-intuitivement, le modèle le plus simple s'avère être le plus performant sur ce dataset. Nous avons donc choisi la régression logistique pour la production en raison de :
- **Meilleure accuracy** (78.03% vs 77.82% pour BERT et 77.51% pour BiLSTM)
- **Rapidité exceptionnelle** : entraînement en 12 secondes, inférence < 10ms
- **Interprétabilité** : on peut expliquer chaque prédiction (mots discriminants)
- **Coûts minimaux** : pas de GPU nécessaire, modèle < 10 MB
- Les modèles complexes (BiLSTM, BERT) sont gardés en réserve pour des cas d'usage futurs nécessitant une compréhension contextuelle plus fine

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

**Exemple de tracking pour le modèle BiLSTM :**
```python
mlflow.log_params({
    "model_type": "BiLSTM_Word2Vec_Stem",
    "embedding_dim": 300,
    "lstm_units": 128,
    "dropout_rate": 0.5,
    "batch_size": 64,
    "learning_rate": 0.001,
    "preprocessing": "stemming"
})

mlflow.log_metrics({
    "test_accuracy": 0.7751,
    "test_f1_score": 0.7777,
    "test_roc_auc": 0.8585,
    "training_time_sec": 1842.3,
    "model_size_mb": 48.3
})
```

**Avantages :**
- Vue centralisée de toutes les expérimentations (50+ runs dans notre cas)
- Comparaison visuelle des hyperparamètres et résultats
- Traçabilité complète : qui a lancé quel modèle, quand, avec quels paramètres

**Interface MLflow UI :**

L'interface web MLflow (accessible sur `http://localhost:5001`) nous permet de :
- Filtrer les runs par métrique (ex: accuracy > 0.75)
- Comparer visuellement les courbes d'apprentissage
- Identifier rapidement les meilleurs modèles
- Télécharger les artefacts (modèles sauvegardés, graphiques)

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

### 5. Déploiement de l'API FastAPI

**Architecture de déploiement :**

L'API FastAPI peut être déployée sur différentes plateformes :
- **Railway** : déploiement simplifié avec détection automatique
- **Heroku** : plateforme PaaS classique
- **Docker** : conteneurisation pour portabilité maximale
- **Local** : développement et tests

**Configuration :**
```python
# Lancement avec Uvicorn
uvicorn api.app:app --host 0.0.0.0 --port $PORT
```

**Variables d'environnement :**
- `MODEL_TYPE` : type de modèle (logistic, lstm, bert)
- `MODEL_PATH` : chemin vers le modèle sérialisé
- `PORT` : port d'écoute (défaut 8000)

**API endpoints :**
- `GET /health` : vérification de l'état de santé
- `POST /predict` : prédiction pour un tweet unique
- `POST /predict/batch` : prédictions batch (jusqu'à 100 tweets)
- `GET /models` : liste des modèles disponibles

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

**Métriques surveillées via PostHog :**
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

Ce projet d'analyse de sentiment pour Air Paradis illustre une démarche MLOps complète, de l'expérimentation à la production. Les trois approches comparées (TF-IDF, BiLSTM, BERT) offrent des performances très similaires (~77-78% accuracy), avec une conclusion surprenante :

- **TF-IDF + Régression Logistique** : meilleure performance (78.03%), rapidité exceptionnelle (choix production)
- **Word2Vec + BiLSTM** : performances légèrement inférieures (77.51%), coût d'entraînement élevé
- **BERT** : meilleur ROC-AUC (0.8622) mais F1-score plus faible, très coûteux en ressources

Ce résultat rappelle qu'un modèle simple bien conçu peut surpasser des approches complexes, surtout sur des tâches de classification binaire avec des textes courts.

L'industrialisation via MLOps (MLflow, Git, tests automatiques, CI/CD, monitoring) garantit la pérennité et la fiabilité du système. Le suivi continu avec PostHog et la stratégie d'amélioration itérative assurent l'adaptation du modèle aux évolutions du langage et des besoins métier.

Cette approche méthodologique est applicable à tout projet de ML en entreprise, quel que soit le domaine d'application. Le MLOps n'est plus une option mais une nécessité pour transformer les expérimentations data science en valeur business durable.

---

**Liens utiles :**
- Interface Streamlit : https://airparadis-sentiment.streamlit.app
- Repository GitHub : https://github.com/tminichetti/openclassrooms-projet7
- API : déployable localement ou sur Railway/Heroku
- MLflow UI : http://localhost:5001 (en local)

**Mots-clés :** MLOps, Deep Learning, NLP, Sentiment Analysis, BERT, LSTM, Word2Vec, MLflow, FastAPI, Heroku, PostHog

**Nombre de mots :** ~1950
