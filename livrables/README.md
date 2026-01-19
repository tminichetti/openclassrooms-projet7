# Livrables - Projet Air Paradis Sentiment Analysis

Ce dossier contient l'ensemble des livrables du projet.

## Structure des notebooks

```
livrables/
├── notebooks/
│   ├── 01_preparation_donnees/     # Exploration et prétraitement des données
│   │   ├── 01_exploration_donnees.ipynb
│   │   └── 02_preprocessing.ipynb
│   │
│   ├── 02_modele_classique/        # Approche simple (TF-IDF + Régression Logistique)
│   │   └── 03_modele_simple_logistique.ipynb
│   │
│   ├── 03_modele_avance/           # Approche avancée (LSTM, CNN, Word2Vec, GloVe)
│   │   └── 04_modele_avance_deep_learning.ipynb
│   │
│   ├── 04_modele_bert/             # Approche BERT (Transfer Learning)
│   │   └── 05_modele_bert.ipynb
│   │
│   └── 05_resultats/               # Graphiques et comparaisons
│       ├── confusion_matrix_logistic.png
│       ├── roc_curve_logistic.png
│       ├── models_comparison_final.png
│       ├── bert_confusion_matrix.png
│       └── ...
│
├── ARTICLE_BLOG_MLOPS.md           # Article de blog sur la démarche MLOps
├── PLAN_PRESENTATION_20MIN.md      # Plan détaillé pour la soutenance
├── TWEETS_DEMO.md                  # Tweets pour la démonstration
└── README.md                       # Ce fichier
```

## Les 3 approches de modélisation

### 1. Modèle classique (baseline)
**Notebook** : `02_modele_classique/03_modele_simple_logistique.ipynb`

- Vectorisation TF-IDF
- Régression Logistique
- Résultats : ~78% accuracy

### 2. Modèle avancé (Deep Learning)
**Notebook** : `03_modele_avance/04_modele_avance_deep_learning.ipynb`

- Embeddings : Word2Vec et GloVe testés
- Prétraitements : Lemmatization et Stemming testés
- Architectures : Bi-LSTM et CNN
- Résultats : ~77% accuracy

### 3. Modèle BERT (Transfer Learning)
**Notebook** : `04_modele_bert/05_modele_bert.ipynb`

- Modèle pré-entraîné : bert-base-uncased
- Fine-tuning sur nos données
- Résultats : ~78% accuracy

## Tracking MLFlow

Toutes les expérimentations sont trackées avec MLFlow :
- Paramètres (embedding_dim, lstm_units, dropout, etc.)
- Métriques (accuracy, F1-score, ROC-AUC, temps d'entraînement)
- Artefacts (graphiques, modèles sauvegardés)

Pour visualiser les runs :
```bash
mlflow ui --backend-store-uri file:///home/thomas/mlruns
```

## Autres livrables

- **API déployée** : https://openclassrooms-projet7-5e5ebd15aa21.herokuapp.com
- **Interface Streamlit** : Déployée sur Streamlit Cloud
- **Code source** : Dossiers `api/` et `streamlit/` à la racine du projet
