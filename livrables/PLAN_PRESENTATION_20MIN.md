# Plan de Présentation - Projet 7 Air Paradis (20 minutes)

## Structure (timing indicatif)

| Section | Durée | Contenu |
|---------|-------|---------|
| Introduction | 2 min | Contexte et objectifs |
| Données et prétraitement | 3 min | Exploration, nettoyage, NLTK |
| Modèles comparés | 6 min | Logistique, Deep Learning, BERT |
| MLOps | 4 min | MLflow tracking, versioning |
| Résultats et choix | 3 min | Synthèse et justification |
| Conclusion | 2 min | Bilan et questions |

---

## DIAPO 1 : Titre (0:30)

**Titre :** Analyse de Sentiment des Tweets - Projet Air Paradis

**Contenu :**
- Votre nom
- Date
- Projet 7 - Parcours Data Scientist OpenClassrooms

**À dire :**
> "Bonjour, je vais vous présenter mon projet d'analyse de sentiment des tweets pour Air Paradis. L'objectif est de développer un système capable de classifier automatiquement les tweets en positif ou négatif, en comparant plusieurs approches de NLP."

---

## DIAPO 2 : Contexte et Problématique (1:30)

**Titre :** Le défi d'Air Paradis

**Contenu :**
- **Contexte :** Compagnie aérienne recevant des milliers de tweets/jour
- **Problème :** Analyse manuelle impossible, besoin d'automatisation
- **Dataset :** Sentiment140 - 1.6 million de tweets annotés
- **Objectif :** Classifier les tweets (positif/négatif) avec haute précision

**Enjeux métier :**
- Détection rapide des insatisfactions clients
- Priorisation des réponses du service client
- Veille sur l'image de marque

**À dire :**
> "Air Paradis souhaite automatiser l'analyse des tweets mentionnant leur marque. J'utilise le dataset Sentiment140 de 1.6 million de tweets pour entraîner et comparer différents modèles de classification de sentiments."

---

## DIAPO 3 : Exploration des Données (1:30)

**Titre :** Analyse exploratoire du dataset

**Contenu (résultats du notebook 01) :**
- **Volume :** 1,600,000 tweets
- **Distribution :** 50% négatifs / 50% positifs (équilibré)
- **659,775 utilisateurs uniques**
- **Période :** Avril - Juin 2009

**Caractéristiques des textes :**
- Longueur moyenne : 74 caractères, 13 mots
- 46.7% contiennent des mentions (@)
- 2.3% contiennent des hashtags (#)
- 4.4% contiennent des URLs

**Visuels :** Graphiques de distribution des sentiments, histogrammes de longueur

**À dire :**
> "Le dataset est parfaitement équilibré avec 800,000 tweets positifs et 800,000 négatifs. Les tweets sont courts, en moyenne 13 mots, et près de la moitié contiennent des mentions d'utilisateurs qu'il faudra nettoyer."

---

## DIAPO 4 : Prétraitement avec NLTK (1:30)

**Titre :** Nettoyage et préparation des données

**Contenu (résultats du notebook 02) :**

**Étapes de nettoyage :**
1. Suppression des doublons : 18,534 tweets (-1.16%)
2. Suppression URLs, mentions, hashtags
3. Tokenisation avec `RegexpTokenizer`
4. Suppression stopwords (198 mots anglais)
5. **Lemmatisation** avec `WordNetLemmatizer`
6. **Stemming** avec `SnowballStemmer` (pour comparaison)

**Résultats :**
- Dataset après nettoyage : **1,385,537 tweets**
- Longueur moyenne après : 41 caractères, 6.7 mots
- Splits : Train 70% / Val 15% / Test 15%

**Exemple :**
```
AVANT : @user I love this movie! http://example.com #awesome
APRÈS : love movie awesome
```

**À dire :**
> "Le prétraitement avec NLTK comprend tokenisation, suppression des stopwords, et normalisation. J'ai comparé deux approches : la lemmatisation qui préserve le sens des mots, et le stemming plus agressif. Le dataset final contient 1.38 million de tweets propres."

---

## DIAPO 5 : Modèle Simple - Régression Logistique (2:00)

**Titre :** Baseline : TF-IDF + Régression Logistique

**Contenu (résultats du notebook 03) :**

**Architecture :**
- Vectorisation TF-IDF (10,000 features, bigrammes)
- Régression Logistique (solver LBFGS)
- Temps d'entraînement : **11.6 secondes**

**Performances sur Test Set :**
| Métrique | Score |
|----------|-------|
| **Accuracy** | **78.03%** |
| Precision | 76.86% |
| Recall | 79.38% |
| F1-Score | 78.10% |
| ROC-AUC | 86.08% |

**Interprétabilité :**
- Top features positives : "can wait", "cant wait", "thank", "glad"
- Top features négatives : "sad", "bummed", "sick", "disappointed"

**À dire :**
> "Le modèle baseline atteint 78% d'accuracy en seulement 12 secondes d'entraînement. C'est une excellente référence. L'avantage de ce modèle est son interprétabilité : on peut voir quels mots influencent le plus la prédiction."

---

## DIAPO 6 : Modèles Avancés - Deep Learning (2:00)

**Titre :** Comparaison des approches Deep Learning

**Contenu (résultats du notebook 04) :**

**Expérimentations réalisées :**
1. **Bi-LSTM + Word2Vec + Lemmatisation**
2. **Bi-LSTM + Word2Vec + Stemming**
3. **Bi-LSTM + GloVe + Lemmatisation**
4. **CNN + GloVe + Lemmatisation**

**Résultats comparatifs (Test Set) :**
| Modèle | Accuracy | F1-Score | ROC-AUC |
|--------|----------|----------|---------|
| BiLSTM + W2V + Lemma | 77.25% | 77.02% | 85.52% |
| **BiLSTM + W2V + Stem** | **77.51%** | **77.77%** | **85.85%** |
| BiLSTM + GloVe + Lemma | 76.56% | 76.47% | 84.77% |
| CNN + GloVe + Lemma | 74.74% | 73.86% | 82.91% |

**Conclusions :**
- **Stemming > Lemmatisation** (+0.75% F1)
- **Word2Vec > GloVe** (+0.55% F1) - Word2Vec entraîné sur nos données
- **Bi-LSTM > CNN** (+2.61% F1) - Meilleure capture du contexte séquentiel

**À dire :**
> "J'ai testé 4 combinaisons différentes pour respecter les critères d'évaluation : 2 prétraitements, 2 embeddings, 2 architectures. Le meilleur modèle est le Bi-LSTM avec Word2Vec et stemming, atteignant 77.77% de F1-score."

---

## DIAPO 7 : Modèle BERT (2:00)

**Titre :** Fine-tuning BERT pour la classification

**Contenu (résultats du notebook 05) :**

**Configuration :**
- Modèle : `bert-base-uncased` (110M paramètres)
- Dataset : 100,000 tweets (pour temps raisonnable)
- Régularisation : Dropout 0.3, 8 couches freezées
- Entraînement : 25 epochs, ~5h sur GPU

**Performances sur Test Set :**
| Métrique | Score |
|----------|-------|
| **Accuracy** | **77.82%** |
| Precision | 79.13% |
| Recall | 75.12% |
| F1-Score | 77.07% |
| ROC-AUC | 86.22% |

**Exemples de prédictions :**
- "This flight was amazing!" → Positif (98.6% confiance)
- "Terrible service, never flying again" → Négatif (97.5% confiance)
- "Delayed for 5 hours, worst airline" → Négatif (99.1% confiance)

**À dire :**
> "BERT atteint 77.82% d'accuracy avec un très bon ROC-AUC de 86.22%. Le modèle montre une excellente confiance sur les cas clairs. Cependant, l'entraînement a nécessité 5 heures sur GPU contre quelques minutes pour les autres modèles."

---

## DIAPO 8 : Tracking MLflow (2:00)

**Titre :** Suivi des expérimentations avec MLflow

**Contenu :**

**Métriques trackées pour chaque run :**
- Hyperparamètres (embedding_dim, lstm_units, dropout, learning_rate)
- Métriques de performance (accuracy, F1, precision, recall, ROC-AUC)
- Temps d'entraînement
- Courbes d'apprentissage
- Artefacts (modèles, visualisations)

**Expérience : `sentiment-analysis-twitter`**
- Modèle simple : 1 run
- Modèles avancés : 4 runs
- Modèle BERT : 1 run

**Avantages MLflow :**
- Reproductibilité des expérimentations
- Comparaison visuelle des hyperparamètres
- Versioning des modèles
- Facilité de collaboration

**Visuels :**
- **CAPTURE :** Interface MLflow UI avec liste des runs
- **CAPTURE :** Graphiques de comparaison

**À dire :**
> "MLflow m'a permis de tracker toutes mes expérimentations de manière structurée. Chaque run enregistre automatiquement les hyperparamètres et métriques, ce qui facilite la comparaison et garantit la reproductibilité."

---

## DIAPO 9 : Versioning et Collaboration (2:00)

**Titre :** Organisation du projet

**Contenu :**

**Structure du repository :**
```
openclassrooms-projet7/
├── livrables/
│   └── notebooks/
│       ├── 01_preparation_donnees/
│       │   ├── 01_exploration_donnees.ipynb
│       │   └── 02_preprocessing.ipynb
│       ├── 02_modele_classique/
│       │   └── 03_modele_simple_logistique.ipynb
│       ├── 03_modele_avance/
│       │   └── 04_modele_avance_deep_learning.ipynb
│       └── 04_modele_bert/
│           └── 05_modele_bert.ipynb
├── data/
│   ├── processed/    # Données prétraitées
│   └── glove.6B.100d.txt
└── models/           # Modèles sauvegardés
```

**Points clés :**
- Code versionné sur GitHub
- Notebooks numérotés et organisés par étape
- Données prétraitées sauvegardées pour reproductibilité
- Modèles exportables (joblib, h5, pretrained)

**À dire :**
> "Le projet est organisé de manière claire avec les notebooks numérotés suivant le flux de travail : exploration, prétraitement, puis les trois types de modèles. Les données prétraitées sont sauvegardées pour garantir la reproductibilité."

---

## DIAPO 10 : Tableau Comparatif Final (2:00)

**Titre :** Synthèse des performances

**Contenu :**

| Critère | Régression Log. | BiLSTM + W2V | BERT |
|---------|-----------------|--------------|------|
| **Accuracy** | 78.03% | 77.51% | 77.82% |
| **F1-Score** | 78.10% | 77.77% | 77.07% |
| **ROC-AUC** | 86.08% | 85.85% | **86.22%** |
| **Temps entraînement** | **12 sec** | ~30 min | ~5h |
| **Taille modèle** | **< 10 MB** | ~50 MB | ~500 MB |
| **Interprétabilité** | **Excellente** | Faible | Faible |
| **Complexité déploiement** | **Facile** | Moyenne | Difficile |

**Observations clés :**
- Performances très proches (< 1% de différence)
- La régression logistique reste compétitive !
- BERT nécessite beaucoup plus de ressources pour un gain marginal
- Le meilleur ROC-AUC est obtenu par BERT (86.22%)

**À dire :**
> "Les trois approches atteignent des performances très similaires, autour de 77-78% d'accuracy. La régression logistique offre le meilleur rapport performance/coût avec un entraînement en 12 secondes et une excellente interprétabilité."

---

## DIAPO 11 : Choix du Modèle pour Production (1:00)

**Titre :** Recommandation pour Air Paradis

**Contenu :**

**Modèle recommandé : Régression Logistique TF-IDF**

**Justification :**
1. **Performance équivalente** : 78% accuracy (meilleur score)
2. **Rapidité** : Entraînement en 12 secondes, inférence < 10ms
3. **Interprétabilité** : On peut expliquer pourquoi un tweet est classé
4. **Facilité de déploiement** : Fichier < 10 MB, pas de GPU requis
5. **Maintenance simple** : Ré-entraînement rapide avec nouvelles données

**Alternative selon le contexte :**
- Si **précision maximale** requise → BERT (ROC-AUC 86.22%)
- Si **temps réel** et **gros volume** → Régression Logistique
- Si **ressources GPU disponibles** → BiLSTM ou BERT

**À dire :**
> "Je recommande la régression logistique pour la production. Avec 78% d'accuracy et un temps d'inférence inférieur à 10ms, c'est le meilleur choix pour traiter de gros volumes en temps réel. Les modèles deep learning sont gardés en réserve pour des cas nécessitant une précision maximale."

---

## DIAPO 12 : Limitations et Perspectives (1:00)

**Titre :** Limites et améliorations futures

**Contenu :**

**Limitations actuelles :**
- Sarcasme et ironie difficiles à détecter
- Dataset de 2009 (vocabulaire peut être daté)
- Uniquement tweets en anglais
- Classification binaire (pas de neutre)

**Perspectives d'amélioration :**
1. **Données récentes** : Collecter des tweets Air Paradis actuels
2. **Multi-classe** : Ajouter sentiment neutre/mixte
3. **Multilingue** : Support français, espagnol
4. **Aspects** : Sentiment par sujet (service, prix, confort)
5. **API de déploiement** : FastAPI + Docker + monitoring

**À dire :**
> "Le modèle a des limitations, notamment sur le sarcasme et les données datant de 2009. Les prochaines étapes seraient de collecter des données récentes spécifiques à Air Paradis et de déployer une API de production avec monitoring."

---

## DIAPO 13 : Synthèse des Livrables (0:30)

**Titre :** Récapitulatif des livrables

**Contenu :**

**Notebooks :**
- 01_exploration_donnees.ipynb - Analyse exploratoire
- 02_preprocessing.ipynb - Nettoyage NLTK
- 03_modele_simple_logistique.ipynb - Baseline
- 04_modele_avance_deep_learning.ipynb - LSTM/CNN
- 05_modele_bert.ipynb - Transfer learning

**Critères d'évaluation couverts :**
- 2 prétraitements comparés (Lemma vs Stem)
- 2 word embeddings comparés (Word2Vec vs GloVe)
- 2+ architectures deep learning (Bi-LSTM, CNN)
- Au moins 1 modèle LSTM
- Tracking MLflow complet

**À dire :**
> "Tous les livrables sont présents : 5 notebooks couvrant l'ensemble du pipeline, avec les comparaisons requises et le tracking MLflow."

---

## DIAPO 14 : Conclusion (1:00)

**Titre :** Bilan du projet

**Contenu :**

**Résumé :**
1. Dataset Sentiment140 : 1.6M tweets, équilibré
2. Prétraitement NLTK rigoureux (tokenisation, lemmatisation, stemming)
3. 3 approches comparées : Classique, Deep Learning, Transformers
4. Performances similaires (~77-78% accuracy)
5. Régression logistique recommandée pour production

**Apprentissages clés :**
- Les modèles simples restent compétitifs face au deep learning
- Le prétraitement est crucial pour les performances
- MLflow facilite grandement le suivi des expérimentations
- Le choix du modèle dépend du contexte (coût, volume, interprétabilité)

**Message final :**
> "La complexité d'un modèle ne garantit pas de meilleures performances. Le bon modèle est celui qui répond au besoin métier avec le meilleur rapport performance/coût."

**À dire :**
> "En conclusion, ce projet montre qu'un modèle classique bien conçu peut rivaliser avec le deep learning. Le choix final doit intégrer les contraintes métier : volume, latence, interprétabilité et coûts d'infrastructure."

---

## DIAPO 15 : Questions (2:00+)

**Titre :** Merci - Questions ?

**Contenu :**
- Liens vers le repository GitHub
- Contact

---

## Questions Fréquentes à Préparer

**Q1 : Pourquoi la régression logistique bat les modèles deep learning ?**
> Le dataset est relativement simple (textes courts, classification binaire). TF-IDF capture efficacement les mots-clés discriminants. Les modèles complexes n'apportent pas de gain significatif sur ce type de tâche.

**Q2 : Pourquoi Word2Vec bat GloVe ?**
> Word2Vec est entraîné directement sur nos tweets, donc les embeddings sont adaptés au vocabulaire Twitter (abréviations, style informel). GloVe est pré-entraîné sur des textes plus formels.

**Q3 : Comment gérer le sarcasme ?**
> C'est un problème ouvert en NLP. Des pistes : modèles spécialisés sur le sarcasme, analyse du contexte (historique utilisateur), indices multimodaux (émojis, ponctuation excessive).

**Q4 : Pourquoi BERT ne performe pas mieux ?**
> Plusieurs raisons : dataset de 2009 avec vocabulaire différent des données de pré-entraînement de BERT, tweets courts limitant l'avantage du contexte bidirectionnel, et possible sous-entraînement (100k tweets vs 1.6M pour les autres).

**Q5 : Comment améliorer les performances ?**
> - Données plus récentes et spécifiques à Air Paradis
> - Augmentation de données (paraphrase, back-translation)
> - Ensemble de modèles (voting)
> - Fine-tuning BERT sur plus de données

**Q6 : Quel est le temps d'inférence en production ?**
> Régression logistique : < 10ms par tweet. BERT : ~200ms par tweet. Pour 10,000 tweets/jour, la régression traite tout en < 2 minutes, BERT en ~30 minutes.

---

## Checklist Avant Présentation

### Technique
- [ ] Notebooks exécutés avec outputs visibles
- [ ] Captures d'écran MLflow préparées
- [ ] Métriques vérifiées et cohérentes

### Contenu
- [ ] Relire le plan
- [ ] Préparer les slides PowerPoint
- [ ] Vérifier orthographe

### Timing
- [ ] Répéter la présentation (chronométrer)
- [ ] Identifier sections à raccourcir si retard
- [ ] Préparer version 15 min si besoin

---

## Récapitulatif Timing

| Temps | Slide | Section |
|-------|-------|---------|
| 2 min | 2 | Contexte terminé |
| 5 min | 4 | Données terminées |
| 11 min | 7 | Modèles terminés |
| 15 min | 9 | MLOps terminé |
| 18 min | 12 | Résultats terminés |
| 20 min | 15 | Questions |

---

Bonne soutenance !
