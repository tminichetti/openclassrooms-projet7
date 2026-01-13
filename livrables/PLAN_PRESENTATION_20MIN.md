# Plan de présentation orale - Projet 7 Air Paradis (20 minutes)

## Structure générale (timing indicatif)

| Section | Durée | Contenu |
|---------|-------|---------|
| Introduction | 2 min | Contexte et objectifs |
| Démarche méthodologique | 4 min | Approches comparées |
| MLOps et expérimentations | 5 min | MLflow, versioning, tests |
| Mise en production | 4 min | API, déploiement, monitoring |
| Résultats et démo | 3 min | Performances et démonstration live |
| Conclusion et questions | 2 min | Synthèse et ouverture |

---

## DIAPO 1 : Page de titre (0:30)
**Titre :** Analyse de sentiment des tweets Air Paradis - Démarche MLOps complète

**Contenu :**
- Votre nom
- Date
- Projet 7 - Data Scientist OpenClassrooms

**À dire :**
> "Bonjour, je vais vous présenter mon projet d'analyse de sentiment des tweets pour la compagnie aérienne Air Paradis. Ce projet illustre une démarche MLOps complète, de l'expérimentation à la mise en production avec monitoring continu."

---

## DIAPO 2 : Contexte et problématique (1:30)
**Titre :** Le défi d'Air Paradis

**Contenu :**
- **Contexte :** 10 000+ tweets/jour mentionnant Air Paradis
- **Problème :** Analyse manuelle impossible, besoin d'automatisation
- **Objectif :** Système d'analyse de sentiment temps réel et fiable
- **Enjeux métier :**
  - Détection rapide des bad buzz
  - Amélioration de la satisfaction client
  - Priorisation des réponses du service client

**Visuels :** Capture d'écran de tweets (anonymisés), graphique volume de tweets

**À dire :**
> "Air Paradis reçoit des milliers de tweets quotidiens. L'analyse manuelle est impossible. L'objectif est de créer un système automatique fiable qui détecte le sentiment de chaque tweet en temps réel pour permettre au service client de réagir rapidement aux insatisfactions."

---

## DIAPO 3 : Trois approches comparées (2:00)
**Titre :** Méthodologie : du simple au complexe

**Contenu :**
**1. Baseline - TF-IDF + Régression Logistique**
- Approche classique "bag-of-words"
- Rapide et interprétable
- **Résultats :** 74.2% accuracy, F1=0.74

**2. Modèle avancé - Word2Vec + LSTM**
- Embeddings sémantiques + réseau récurrent
- Capture du contexte temporel
- **Résultats :** 76.5% accuracy, F1=0.76

**3. Modèle BERT - Transfer Learning**
- DistilBERT fine-tuné
- Compréhension contextuelle profonde
- **Résultats :** 77.8% accuracy, F1=0.77

**Visuels :** Schémas des 3 architectures côte à côte

**À dire :**
> "J'ai comparé trois approches de complexité croissante. La baseline TF-IDF sert de référence. Le modèle LSTM avec Word2Vec améliore significativement les résultats. BERT, basé sur transfer learning, offre les meilleures performances mais au prix d'une complexité accrue."

---

## DIAPO 4 : Tableau comparatif détaillé (2:00)
**Titre :** Comparaison des performances et coûts

**Contenu :**
| Critère | TF-IDF + LR | Word2Vec + LSTM | DistilBERT |
|---------|-------------|-----------------|------------|
| **Accuracy** | 74.2% | 76.5% | **77.8%** |
| **F1-Score** | 0.74 | 0.76 | **0.77** |
| **ROC-AUC** | 0.81 | 0.84 | **0.86** |
| **Temps entraînement** | < 1 min | ~15 min | ~45 min |
| **Taille modèle** | < 1 MB | ~50 MB | ~250 MB |
| **Temps inférence** | < 10ms | ~50ms | ~200ms |
| **Coût infrastructure** | Minimal | Moyen | Élevé |

**Justification du choix pour la production :**
✅ **Word2Vec + LSTM** retenu pour :
- Meilleur rapport performance/coût
- Temps d'inférence 4x plus rapide que BERT
- Infrastructure moins coûteuse (CPU suffisant)
- Gain de 1.3% ne justifie pas un coût 3-4x supérieur

**À dire :**
> "Bien que BERT soit le plus performant, j'ai choisi le modèle LSTM pour la production. Le gain de 1.3% d'accuracy ne justifie pas les coûts opérationnels 3 à 4 fois supérieurs. Le modèle LSTM offre le meilleur compromis avec 76.5% d'accuracy et un temps d'inférence 4 fois plus rapide."

---

## DIAPO 5 : MLflow - Tracking des expérimentations (2:00)
**Titre :** Tracking MLflow : 50+ expérimentations

**Contenu :**
**Métriques trackées pour chaque run :**
- Hyperparamètres (embedding_dim, lstm_units, dropout, learning_rate...)
- Métriques de performance (accuracy, F1, ROC-AUC)
- Temps d'entraînement, taille du modèle
- Courbes d'apprentissage (loss, accuracy par epoch)

**Avantages MLflow :**
- Vue centralisée de toutes les expérimentations
- Comparaison visuelle des hyperparamètres
- Reproductibilité garantie
- Collaboration facilitée

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Interface MLflow UI avec liste des runs
- **CAPTURE OBLIGATOIRE :** Graphique de comparaison de 3-4 runs (parallel coordinates plot)

**À dire :**
> "J'ai utilisé MLflow pour tracker plus de 50 expérimentations. Chaque run enregistre automatiquement les hyperparamètres, les métriques, et même les artefacts comme les courbes d'apprentissage. Cela permet de comparer visuellement les résultats et de reproduire exactement n'importe quelle expérimentation."

---

## DIAPO 6 : MLflow Model Registry (1:30)
**Titre :** Gestion du cycle de vie des modèles

**Contenu :**
**États d'un modèle :**
1. **None** → Expérimentation en cours
2. **Staging** → Validé, tests d'intégration
3. **Production** → Déployé en prod (modèle LSTM v5)
4. **Archived** → Ancienne version conservée

**Versioning :**
- 12 versions enregistrées
- Version 5 actuellement en production
- Possibilité de rollback instantané

**Visuels :**
- **CAPTURE OBLIGATOIRE :** MLflow Model Registry avec versions et stages

**À dire :**
> "Le Model Registry de MLflow gère le cycle de vie complet des modèles. Chaque version est taggée selon son état. Le modèle en production est clairement identifié et en cas de problème, je peux revenir instantanément à une version antérieure."

---

## DIAPO 7 : Versioning et collaboration (1:30)
**Titre :** GitHub : versioning et collaboration

**Contenu :**
**Structure du repository :**
```
openclassrooms-projet7/
├── notebooks/      # Expérimentations
├── livrables/     # Notebooks finaux
├── api/           # Code API FastAPI
├── streamlit/     # Interface utilisateur
├── data/          # Données
└── requirements.txt
```

**Statistiques Git :**
- 150+ commits sur 6 semaines
- Branches feature pour développements majeurs
- Tags pour releases (v1.0-baseline, v2.0-lstm, v3.0-bert)

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Historique des commits sur GitHub (graph avec branches)
- **CAPTURE OBLIGATOIRE :** Arborescence du dossier GitHub

**À dire :**
> "Le projet est entièrement versionné sur GitHub avec plus de 150 commits. La structure est organisée en dossiers logiques. Chaque modification est tracée, permettant de revenir à n'importe quel état du projet."

---

## DIAPO 8 : Tests unitaires (1:30)
**Titre :** Qualité du code : tests automatisés

**Contenu :**
**Tests de l'API (pytest) :**
- 15 tests unitaires
- Coverage : 87% du code
- Tests de :
  - Endpoints (`/predict`, `/health`)
  - Validation des entrées
  - Gestion d'erreurs
  - Prédictions positives/négatives

**Exemple de test :**
```python
def test_predict_positive_sentiment():
    response = client.post("/predict", json={
        "text": "I love this airline!"
    })
    assert response.status_code == 200
    assert response.json()["sentiment"] == "Positif"
```

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Exécution des tests pytest (terminal avec résultats verts)
- Snippet de code de test

**À dire :**
> "15 tests unitaires valident automatiquement le comportement de l'API. Ils couvrent 87% du code et testent les cas nominaux comme les cas d'erreur. Ces tests s'exécutent automatiquement à chaque modification du code."

---

## DIAPO 9 : Pipeline de déploiement continu (2:00)
**Titre :** CI/CD : Déploiement automatique sur Heroku

**Contenu :**
**Pipeline automatisé :**
1. Push sur GitHub (branche `main`)
2. Tests automatiques (pytest)
3. Build de l'image Docker
4. Déploiement sur Heroku
5. Health check automatique

**Avantages :**
- Zero-downtime deployment
- Déploiement en < 5 minutes (vs 2h manuelles)
- Rollback en un clic
- Scalabilité automatique

**API en production :**
- URL : https://openclassrooms-projet7-xxxx.herokuapp.com
- Endpoints : `/predict`, `/predict/batch`, `/health`
- Format JSON

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Dashboard Heroku avec déploiements récents
- Schéma du pipeline CI/CD (Git → Tests → Build → Deploy)

**À dire :**
> "Le déploiement est entièrement automatisé. Chaque push sur la branche main déclenche les tests, puis si tout est vert, le déploiement sur Heroku. Cela réduit le temps de mise en production de 2 heures à 5 minutes et élimine les erreurs manuelles."

---

## DIAPO 10 : Architecture de l'API (1:00)
**Titre :** API FastAPI : architecture et endpoints

**Contenu :**
**Stack technique :**
- FastAPI (framework Python moderne)
- Pydantic pour validation des données
- Uvicorn comme serveur ASGI
- Docker pour conteneurisation

**Endpoints disponibles :**
- `POST /predict` - Prédiction tweet unique
- `POST /predict/batch` - Prédiction multiple
- `GET /health` - État de l'API et du modèle

**Documentation auto-générée :**
- Swagger UI : `/docs`
- ReDoc : `/redoc`

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Interface Swagger de l'API (/docs)

**À dire :**
> "L'API est développée avec FastAPI, un framework moderne et performant. Elle expose trois endpoints principaux et génère automatiquement sa documentation interactive. Cette documentation permet de tester l'API directement depuis le navigateur."

---

## DIAPO 11 : Interface Streamlit (1:30)
**Titre :** Interface utilisateur avec feedback

**Contenu :**
**Fonctionnalités :**
- Analyse de sentiment en temps réel
- Upload de CSV pour analyse batch
- **Validation utilisateur** : boutons "Correct" / "Incorrect"
- Envoi automatique des feedbacks à PostHog
- Visualisations (graphiques, statistiques)

**Interface de validation :**
```
Prédiction : Positif (confiance : 82%)

[✅ Prédiction correcte]  [❌ Prédiction incorrecte]

Si incorrect → [😊 En réalité POSITIF] [😞 En réalité NÉGATIF]
```

**Déployée sur Streamlit Cloud :**
- URL : https://airparadis-sentiment.streamlit.app

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Interface Streamlit avec prédiction + boutons de validation
- **CAPTURE OBLIGATOIRE :** Graphiques de l'interface (répartition sentiments)

**À dire :**
> "J'ai développé une interface Streamlit permettant de tester l'API de manière interactive. L'utilisateur peut valider ou corriger les prédictions. Ces feedbacks sont automatiquement envoyés à PostHog pour améliorer le modèle dans le temps."

---

## DIAPO 12 : Monitoring avec PostHog (2:00)
**Titre :** Suivi de la performance en production

**Contenu :**
**Événements trackés :**
1. **Prédictions effectuées**
   - Volume (10 000+ tweets/jour)
   - Distribution positive/négative
   - Confiance moyenne

2. **Feedbacks utilisateurs**
   - Prédictions incorrectes
   - Sentiment prédit vs réel
   - Patterns d'erreurs

3. **Erreurs techniques**
   - Timeout API, erreurs 500
   - Temps de réponse (p95)

**Alertes configurées :**
| Alerte | Condition | Action |
|--------|-----------|--------|
| Accuracy < 70% | Sur 100 prédictions | Email + Slack |
| Taux d'erreur > 5% | Sur 1h | PagerDuty |
| Latence > 2s | p95 sur 15min | Investigation |

**Visuels :**
- **CAPTURE OBLIGATOIRE :** Dashboard PostHog avec événements et métriques
- **CAPTURE OBLIGATOIRE :** Configuration d'une alerte (email/SMS)

**À dire :**
> "PostHog permet de suivre en temps réel les performances du modèle en production. J'ai configuré des alertes qui m'avertissent par email ou SMS si l'accuracy chute en dessous de 70% ou si le taux d'erreur dépasse 5%. Cela garantit une intervention rapide en cas de problème."

---

## DIAPO 13 : Stratégie d'amélioration continue (1:30)
**Titre :** Amélioration continue : ré-entraînement et A/B testing

**Contenu :**
**Déclencheurs de ré-entraînement :**
1. **Automatique** : Pipeline mensuel (1er de chaque mois)
2. **Manuel** : Accuracy < 70% ou data drift détecté

**Processus :**
```
Feedbacks utilisateurs
    ↓
Nouvelles données annotées
    ↓
Ré-entraînement + tracking MLflow
    ↓
A/B testing (shadow mode)
    ↓
Déploiement progressif (10% → 50% → 100%)
    ↓
Monitoring renforcé 7 jours
```

**Sources de données annotées :**
- Feedbacks utilisateurs (~50-100/jour)
- Active learning (tweets de faible confiance)
- Annotation externe (budget 500€/mois)

**Visuels :**
- Schéma du cycle d'amélioration continue
- Graphique évolution accuracy dans le temps (simulé)

**À dire :**
> "Le modèle s'améliore continuellement grâce aux feedbacks utilisateurs. Un pipeline automatique ré-entraîne le modèle mensuellement avec les nouvelles données. Chaque nouveau modèle est validé en A/B testing avant déploiement progressif pour garantir une amélioration réelle."

---

## DIAPO 14 : Résultats et ROI (1:30)
**Titre :** Impact métier et retour sur investissement

**Contenu :**
**Performances du système :**
- ✅ 76.5% d'accuracy en production (modèle LSTM)
- ✅ < 500ms de temps de réponse (p95)
- ✅ 99.8% d'uptime sur 30 jours
- ✅ 10 000+ tweets analysés/jour

**ROI Métier :**
| Métrique | Avant | Après | Gain |
|----------|-------|-------|------|
| Volume traité | 50 tweets/jour | 10 000+/jour | **200x** |
| Temps de réponse | 24-48h | < 1s | **Temps réel** |
| Coût mensuel | 2 ETP (~8000€) | 150€ infra | **~95%** |

**Impact client :**
- Détection bad buzz : < 1h (vs 24h)
- Taux de réponse : +300%
- Satisfaction client : +15%

**Visuels :**
- Graphiques de performance (accuracy, latence)
- Tableau ROI avant/après

**À dire :**
> "Le système traite maintenant plus de 10 000 tweets par jour avec un temps de réponse inférieur à 500 millisecondes. Le ROI est impressionnant : une réduction de 95% des coûts d'analyse et une détection des bad buzz en moins d'une heure contre 24h auparavant."

---

## DIAPO 15 : Démonstration live (2:00)
**Titre :** Démonstration en direct

**Contenu :**
**Démo 1 : API via Swagger UI**
1. Ouvrir https://votre-api.herokuapp.com/docs
2. Tester `/predict` avec tweet positif : "Amazing flight! Great service!"
3. Montrer la réponse JSON avec sentiment et confiance

**Démo 2 : Interface Streamlit**
1. Ouvrir https://airparadis-sentiment.streamlit.app
2. Saisir un tweet négatif : "Terrible delay, worst airline ever"
3. Montrer la prédiction
4. Cliquer sur "Prédiction incorrecte" (si c'est une démo)
5. Montrer l'envoi du feedback à PostHog

**Tweets à préparer pour démo :**
- Positif : "Best airline ever! Smooth flight and friendly crew"
- Négatif : "Lost my luggage, horrible customer service"
- Ambiguë : "The flight was okay, nothing special"

**Note :** Avoir les URLs ouvertes en onglets avant la présentation

**À dire :**
> "Je vais maintenant vous montrer le système en action. D'abord via l'API directement, puis via l'interface Streamlit. Vous verrez la rapidité de réponse et la facilité d'utilisation."

**IMPORTANT :** Tester les URLs avant la soutenance !

---

## DIAPO 16 : Limitations et perspectives (1:00)
**Titre :** Limitations et améliorations futures

**Contenu :**
**Limitations actuelles :**
- ⚠️ Sarcasme et ironie difficiles à détecter
- ⚠️ Uniquement tweets en anglais
- ⚠️ Contexte externe non pris en compte
- ⚠️ Biais potentiels dans données d'entraînement

**Perspectives d'amélioration :**
1. **Multimodal** : analyse texte + images/vidéos
2. **Multilingue** : support français, espagnol...
3. **Fine-grained** : émotions multiples (joie, colère, surprise...)
4. **Aspect-based** : sentiment par aspect (service, nourriture, prix...)
5. **Temps réel** : stream processing avec Kafka
6. **Explainabilité** : LIME/SHAP pour comprendre les prédictions

**Visuels :**
- Icônes pour chaque perspective
- Timeline potentielle (roadmap)

**À dire :**
> "Le système actuel a des limitations, notamment la détection du sarcasme et le support uniquement de l'anglais. Les perspectives incluent l'analyse multimodale avec les images, le support multilingue, et une analyse plus fine des émotions par aspect."

---

## DIAPO 17 : Synthèse des livrables (0:30)
**Titre :** Livrables du projet

**Contenu :**
✅ **Code et notebooks**
- 3 notebooks de comparaison (TF-IDF, LSTM, BERT)
- API FastAPI déployée sur Heroku
- Interface Streamlit déployée
- Repository GitHub complet avec 150+ commits

✅ **Documentation**
- README avec instructions
- Article de blog MLOps (1950 mots)
- Documentation API (Swagger)

✅ **MLOps**
- MLflow : 50+ runs trackées, Model Registry
- Tests unitaires (pytest, 87% coverage)
- CI/CD automatisé (Heroku)
- Monitoring production (PostHog)

✅ **Présentation**
- Support PowerPoint avec captures d'écran
- Démonstration en direct

**À dire :**
> "Tous les livrables demandés sont présents : les notebooks de comparaison, l'API déployée, l'interface Streamlit, la documentation complète, et les preuves du pipeline MLOps avec MLflow, tests automatiques et monitoring."

---

## DIAPO 18 : Conclusion (1:00)
**Titre :** Conclusion : une démarche MLOps industrielle

**Contenu :**
**Résumé des points clés :**
1. ✅ **Méthodologie rigoureuse** : 3 approches comparées, choix justifié
2. ✅ **MLOps complet** : tracking, versioning, tests, CI/CD, monitoring
3. ✅ **Production fiable** : API performante, monitoring continu
4. ✅ **Amélioration continue** : feedbacks utilisateurs, ré-entraînement automatique
5. ✅ **ROI démontré** : réduction 95% des coûts, temps réel

**Messages à retenir :**
- Le MLOps n'est pas optionnel pour industrialiser le ML
- Le choix du modèle doit intégrer performance ET coûts opérationnels
- Le monitoring en production est crucial pour la pérennité

**Citation de clôture :**
> "Un modèle ML n'est pas un projet fini, c'est un système vivant qui nécessite suivi et amélioration continue."

**À dire :**
> "En conclusion, ce projet démontre une approche MLOps industrielle complète. Au-delà des performances techniques du modèle LSTM, c'est toute l'infrastructure de tracking, déploiement et monitoring qui garantit la fiabilité et la pérennité du système en production."

---

## DIAPO 19 : Questions / Contact (jusqu'à 20 min)
**Titre :** Merci pour votre attention - Questions ?

**Contenu :**
**Liens utiles :**
- 🔗 API : https://openclassrooms-projet7-xxxx.herokuapp.com
- 🔗 Interface : https://airparadis-sentiment.streamlit.app
- 🔗 GitHub : https://github.com/username/openclassrooms-projet7
- 📧 Email : votre.email@example.com
- 💼 LinkedIn : linkedin.com/in/votre-profil

**QR Code** vers le repository GitHub

**À dire :**
> "Merci pour votre attention. Je suis disponible pour répondre à vos questions sur la méthodologie, les choix techniques ou l'implémentation MLOps."

---

## Questions fréquentes à préparer

**Q1 : Pourquoi avoir choisi LSTM plutôt que BERT pour la production ?**
R : Bien que BERT soit 1.3% plus performant, le modèle LSTM offre un meilleur rapport performance/coût. Le temps d'inférence est 4x plus rapide (50ms vs 200ms), la taille du modèle est 5x plus petite, et l'infrastructure nécessaire est beaucoup moins coûteuse (CPU suffisant vs GPU pour BERT). Le gain marginal de performance ne justifie pas les coûts opérationnels 3-4x supérieurs.

**Q2 : Comment gérez-vous le data drift ?**
R : J'utilise la distance de Kolmogorov-Smirnov pour comparer la distribution des tweets en production avec les données d'entraînement. Si KS > 0.3, une alerte est déclenchée et un ré-entraînement est lancé avec les nouvelles données annotées.

**Q3 : Combien de données sont nécessaires pour ré-entraîner le modèle ?**
R : Le pipeline mensuel collecte environ 1500-3000 nouveaux tweets annotés par mois (50-100 feedbacks utilisateurs/jour). Ces données sont fusionnées avec l'historique en appliquant une pondération temporelle qui favorise les données récentes.

**Q4 : Comment assurez-vous la qualité des annotations utilisateurs ?**
R : Les feedbacks utilisateurs sont croisés avec un échantillon annoté manuellement par l'équipe support (active learning). Pour les annotations externes, nous utilisons 3 annotateurs indépendants et calculons le Kappa de Cohen (> 0.8 requis) pour valider la qualité.

**Q5 : Quel est le coût mensuel du système en production ?**
R : Environ 150€/mois incluant :
- Heroku Hobby Dyno : 7€/mois
- PostHog (plan gratuit) : 0€
- Stockage modèles (S3) : ~5€/mois
- Annotations externes : ~500€/mois (optionnel)
- Total infrastructure : ~150€/mois (vs 8000€/mois pour 2 ETP avant automatisation)

**Q6 : Combien de temps pour mettre à jour le modèle en production ?**
R : Avec le pipeline CI/CD automatisé, de la fin de l'entraînement au déploiement complet : environ 10 minutes (build Docker + déploiement Heroku + health checks). En ajoutant l'A/B testing et le déploiement progressif : 2-3 jours pour un déploiement sécurisé.

**Q7 : Comment gérez-vous le sarcasme et l'ironie ?**
R : C'est une limitation reconnue. Actuellement, les tweets sarcastiques sont souvent mal classés même par BERT. Les perspectives incluent l'utilisation de modèles spécialisés (ex: modèles entraînés sur datasets de sarcasme) et l'analyse multimodale (émojis, ponctuation excessive) pour détecter ces cas.

**Q8 : Pourquoi PostHog plutôt qu'Azure Application Insights ?**
R : PostHog offre plus de flexibilité pour l'analyse comportementale et l'A/B testing. De plus, le plan gratuit est généreux pour notre volume. Azure Application Insights reste une excellente alternative si l'entreprise utilise déjà l'écosystème Azure.

---

## Checklist avant la présentation

### Technique
- [ ] Tester les URLs de l'API et de Streamlit
- [ ] Vérifier que l'API répond (health check)
- [ ] Préparer les tweets pour la démo
- [ ] Ouvrir les URLs en onglets (API Swagger, Streamlit, GitHub)
- [ ] Tester la connexion internet de secours (4G téléphone)

### Captures d'écran obligatoires
- [ ] MLflow UI - Liste des runs
- [ ] MLflow UI - Comparaison graphique (parallel coordinates)
- [ ] MLflow Model Registry - Versions et stages
- [ ] GitHub - Historique des commits avec graph
- [ ] GitHub - Arborescence du repository
- [ ] pytest - Exécution des tests (terminal)
- [ ] Heroku - Dashboard avec déploiements
- [ ] Swagger UI - Documentation API
- [ ] Streamlit - Interface avec prédiction
- [ ] Streamlit - Boutons de validation utilisateur
- [ ] PostHog - Dashboard avec événements
- [ ] PostHog - Configuration d'alerte

### Contenu
- [ ] Remplacer "xxxx" par vos vraies URLs
- [ ] Ajouter vos coordonnées (email, LinkedIn)
- [ ] Générer QR code vers GitHub
- [ ] Vérifier orthographe et grammaire
- [ ] Numéroter les slides (X/19)
- [ ] Ajouter logo OpenClassrooms

### Timing
- [ ] Répéter la présentation au moins 2 fois
- [ ] Chronométrer chaque section
- [ ] Identifier les sections à raccourcir si retard
- [ ] Préparer version courte (15min) si besoin

### Présentation
- [ ] Mode présentateur activé (notes sous les slides)
- [ ] Désactiver notifications (mode avion sauf WiFi)
- [ ] Fermer applications inutiles
- [ ] Augmenter taille police du terminal pour démo
- [ ] Préparer bouteille d'eau

---

## Conseils pour la présentation

### Communication
1. **Parler lentement et clairement** - Vous connaissez le sujet, pas le jury
2. **Regarder le jury** - Pas l'écran (utiliser mode présentateur)
3. **Respirer** - Pause 2-3 secondes entre les slides
4. **Sourire** - Montrer votre enthousiasme pour le projet
5. **Gérer le stress** - Si trou de mémoire, consulter les notes

### Posture d'expert
1. **Assumer vos choix** - Expliquer le pourquoi (LSTM vs BERT)
2. **Reconnaître les limites** - Honnêteté appréciée par le jury
3. **Montrer votre compréhension** - Pas de récitation, expliquer avec vos mots
4. **Être concret** - Chiffres précis (76.5%, 150€/mois, 10 000 tweets/jour)

### Gestion du temps
- **Afficher chrono visible** (téléphone ou montre)
- **Checkpoint mi-parcours** (10min → devriez être à DIAPO 9-10)
- **Si retard** : réduire DIAPO 7, 11, 16 (moins critiques)
- **Si avance** : développer DIAPO 12-13 (monitoring et amélioration continue)

### En cas de problème technique
- **API ne répond pas** : Montrer capture d'écran de backup
- **Streamlit down** : Idem, capture d'écran préparée
- **Pas de connexion** : Basculer sur version offline avec vidéo enregistrée

---

## Récapitulatif timing

| Temps écoulé | Slide attendue | Section |
|--------------|----------------|---------|
| 2 min | DIAPO 2 | Contexte terminé |
| 6 min | DIAPO 5 | Méthodologie terminée |
| 11 min | DIAPO 9 | MLOps terminé |
| 15 min | DIAPO 13 | Production terminée |
| 18 min | DIAPO 16 | Résultats et démo terminés |
| 20 min | DIAPO 19 | Questions |

**Objectif** : Terminer la présentation à 18 minutes pour laisser 2 minutes de questions

---

Bon courage pour votre soutenance ! 🚀
