# Tweets pour la démonstration - Soutenance Projet 7

## Guide d'utilisation

Pendant la présentation, utilisez ces tweets pour la démonstration live :
1. Copier-coller le tweet dans l'interface Streamlit ou l'API Swagger
2. Observer la prédiction
3. Éventuellement tester le système de validation utilisateur

---

## 1. Tweets clairement POSITIFS ✅

### Tweet 1 - Service excellent
```
Amazing flight experience! The crew was incredibly friendly and helpful. Best airline I've ever flown with. Highly recommend Air Paradis! ⭐⭐⭐⭐⭐
```
**Prédiction attendue** : Positif (confiance élevée ~85-95%)

### Tweet 2 - Vol confortable
```
Just landed after a smooth 8-hour flight. Comfortable seats, great entertainment system, and delicious meals. Thank you Air Paradis for the wonderful journey!
```
**Prédiction attendue** : Positif (confiance élevée ~80-90%)

### Tweet 3 - Excellent rapport qualité-prix
```
Flying with Air Paradis is always a pleasure. Good prices, professional staff, and on-time departures. What more could you ask for?
```
**Prédiction attendue** : Positif (confiance moyenne-élevée ~75-85%)

### Tweet 4 - Service client réactif
```
Lost my phone during the flight but the cabin crew found it within minutes! Such caring and attentive service. Love this airline! 💙
```
**Prédiction attendue** : Positif (confiance élevée ~85-95%)

---

## 2. Tweets clairement NÉGATIFS ❌

### Tweet 5 - Retard important
```
Terrible experience with Air Paradis today. 5-hour delay with no explanation and horrible customer service. Never flying with them again! 😡
```
**Prédiction attendue** : Négatif (confiance élevée ~85-95%)

### Tweet 6 - Bagages perdus
```
Air Paradis lost my luggage for the third time this year! Incompetent staff, no compensation offered. Worst airline ever. Avoid at all costs!
```
**Prédiction attendue** : Négatif (confiance très élevée ~90-98%)

### Tweet 7 - Vol annulé
```
Flight cancelled at the last minute, zero communication from Air Paradis. Had to book another airline and lost $800. Absolutely unacceptable!
```
**Prédiction attendue** : Négatif (confiance élevée ~85-95%)

### Tweet 8 - Conditions à bord
```
The plane was dirty, seats uncomfortable, and no food served on a 6-hour flight. Air Paradis is going downhill fast. Very disappointed. 👎
```
**Prédiction attendue** : Négatif (confiance moyenne-élevée ~75-85%)

---

## 3. Tweets AMBIGUS / MIXTES ⚖️

### Tweet 9 - Sentiment mitigé
```
The flight was okay. Crew was nice but the food could be better. Nothing special, just an average experience with Air Paradis.
```
**Prédiction attendue** : Positif ou Négatif (confiance faible ~50-65%)
**Intérêt** : Cas limite intéressant à montrer au jury

### Tweet 10 - Neutre avec légère critique
```
Air Paradis gets me from A to B. Prices are reasonable but don't expect luxury. It's basic air travel, nothing more.
```
**Prédiction attendue** : Variable (confiance faible-moyenne ~55-70%)
**Intérêt** : Montre les limites du modèle sur sentiments neutres

---

## 4. Tweets avec DIFFICULTÉS SPÉCIFIQUES 🔍

### Tweet 11 - Sarcasme (difficulté connue)
```
Oh great, another Air Paradis delay. Just what I needed today. Thanks for nothing! 🙄
```
**Prédiction attendue** : Risque de mal classifier (possiblement Positif malgré sarcasme)
**Intérêt** : Illustre une limitation connue du modèle
**Note pour le jury** : "Voici un exemple de tweet sarcastique qui peut tromper le modèle. C'est une des limitations que j'ai identifiées."

### Tweet 12 - Émojis négatifs
```
Late again 😤 Air Paradis never learns. Waiting at the gate for 2 hours now 😫😠
```
**Prédiction attendue** : Négatif (les émojis aident)
**Intérêt** : Montre l'importance du traitement des émojis

### Tweet 13 - Très court
```
Air Paradis = worst
```
**Prédiction attendue** : Négatif mais possiblement avec confiance plus faible
**Intérêt** : Performance sur tweets très courts

### Tweet 14 - Beaucoup d'émojis positifs
```
✈️💙 Love love LOVE Air Paradis! 🌟✨ Best crew ever! 😍👏
```
**Prédiction attendue** : Positif (confiance très élevée)
**Intérêt** : Traitement des émojis multiples

---

## 5. Tweets pour tester la VALIDATION UTILISATEUR 👤

### Tweet 15 - Pour tester "Prédiction correcte"
```
Just booked another flight with Air Paradis. They never disappoint! Great airline with excellent customer service.
```
**Action** :
1. Obtenir prédiction (devrait être Positif)
2. Cliquer sur "✅ Prédiction correcte"
3. Montrer le message de confirmation

### Tweet 16 - Pour tester "Prédiction incorrecte"
```
Air Paradis ruined my vacation. Delayed flight, rude staff, and lost luggage. Never again!
```
**Action** :
1. Obtenir prédiction (devrait être Négatif)
2. Cliquer sur "❌ Prédiction incorrecte" (pour la démo)
3. Choisir "😊 En réalité, c'était POSITIF" (même si c'est faux, pour la démo)
4. Montrer que l'événement est envoyé à PostHog

---

## 6. Tweets pour l'analyse BATCH (CSV) 📊

Si vous voulez tester l'upload CSV, créez un fichier `demo_tweets.csv` :

```csv
text
Amazing flight! Best airline ever!
Terrible delay and lost my luggage
The crew was very professional and friendly
Cancelled flight with no compensation
Good value for money, would fly again
Worst customer service I've experienced
Clean plane and comfortable seats
Air Paradis is going downhill fast
Great entertainment system on board
Never booking with them again
```

**Action** :
1. Créer ce fichier CSV
2. L'uploader dans l'interface Streamlit (section "Analyse batch")
3. Montrer les résultats avec graphiques

---

## 7. Scénario de démonstration recommandé (3 minutes)

### Option A : Démonstration via Swagger API (1 min)

**Étape 1** : Ouvrir https://votre-api.herokuapp.com/docs

**Étape 2** : Tester `/predict` avec Tweet 1 (positif)
```json
{
  "text": "Amazing flight experience! The crew was incredibly friendly and helpful. Best airline I've ever flown with."
}
```

**Étape 3** : Montrer la réponse JSON
```json
{
  "sentiment": "Positif",
  "confidence": 0.89,
  "model_type": "lstm_word2vec"
}
```

### Option B : Démonstration via Streamlit (2 min)

**Étape 1** : Ouvrir https://airparadis-sentiment.streamlit.app

**Étape 2** : Tester Tweet 5 (négatif)
```
Terrible experience with Air Paradis today. 5-hour delay with no explanation and horrible customer service.
```

**Étape 3** : Montrer :
- La prédiction (Négatif, ~88% confiance)
- Le graphique de confiance
- Les métriques affichées

**Étape 4** : Tester la validation utilisateur
- Cliquer "❌ Prédiction incorrecte" (pour la démo)
- Choisir "😊 En réalité, c'était POSITIF"
- Montrer le message : "✅ Merci ! Événement envoyé à PostHog"

**Étape 5** : (Optionnel) Montrer un tweet ambigu (Tweet 9) pour illustrer les cas limites

---

## 8. Messages clés à transmettre pendant la démo

Pendant que le modèle traite les tweets, profitez pour expliquer :

### Pour un tweet positif :
> "Comme vous pouvez le voir, le modèle détecte correctement le sentiment positif avec une confiance élevée de 89%. Le temps de réponse est inférieur à 500 millisecondes."

### Pour un tweet négatif :
> "Le tweet contient clairement des mots négatifs comme 'terrible', 'delay', 'horrible'. Le modèle LSTM capture bien ce contexte et prédit correctement un sentiment négatif avec 88% de confiance."

### Pour un tweet ambigu :
> "Voici un cas intéressant : le tweet est assez neutre avec des aspects positifs et négatifs. La confiance est plus faible (65%), ce qui est normal. C'est exactement le type de cas où le feedback utilisateur devient crucial pour améliorer le modèle."

### Pour la validation utilisateur :
> "Grâce à cette fonctionnalité de validation, chaque fois qu'un utilisateur corrige une prédiction, un événement est automatiquement envoyé à PostHog. Ces feedbacks alimentent notre pipeline d'amélioration continue du modèle."

---

## 9. Plan B - En cas de problème technique

Si l'API ou Streamlit ne répondent pas pendant la soutenance :

### Solution 1 : Avoir des captures d'écran de backup
- [ ] Capture : Swagger UI avec requête Tweet 1 → Réponse Positif 89%
- [ ] Capture : Streamlit avec Tweet 5 → Réponse Négatif 88%
- [ ] Capture : Interface de validation utilisateur

### Solution 2 : Tester en local
```bash
# Terminal 1 - Lancer l'API en local
uvicorn api.app:app --reload

# Terminal 2 - Tester avec curl
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing flight! Best airline ever!"}'
```

### Solution 3 : Montrer une vidéo pré-enregistrée
- Enregistrer une vidéo de 30-60 secondes de la démo
- La montrer si problème de connexion

---

## 10. Checklist avant la démo

**24 heures avant :**
- [ ] Tester l'URL de l'API Heroku
- [ ] Tester l'URL de Streamlit Cloud
- [ ] Vérifier que PostHog reçoit bien les événements
- [ ] Ouvrir les URLs dans des onglets (ne pas les fermer)

**1 heure avant :**
- [ ] Re-tester les URLs
- [ ] Copier les tweets 1, 5, et 9 dans un fichier texte pour accès rapide
- [ ] Vérifier la connexion internet (WiFi + 4G backup)
- [ ] Augmenter la taille de police du navigateur si nécessaire

**Pendant la présentation :**
- [ ] Avoir les tweets ouverts dans un notepad/éditeur
- [ ] Ne pas taper les tweets en direct (trop long et risque d'erreur)
- [ ] Copier-coller directement
- [ ] Respirer et parler lentement pendant que le modèle traite

---

## 11. Tweets en français (si demandé par le jury)

**Note** : Le modèle est entraîné sur des tweets en anglais. Si le jury demande un test en français, expliquer :

> "Le modèle actuel est entraîné uniquement sur des tweets en anglais. Une des perspectives d'amélioration serait de créer une version multilingue ou d'entraîner un modèle spécifique pour chaque langue avec un système de détection automatique de la langue."

Vous pouvez quand même tester pour montrer les limites :

### Tweet français positif
```
Vol excellent ! L'équipage était très sympathique. Je recommande Air Paradis !
```
**Prédiction attendue** : Résultats imprévisibles (modèle non entraîné sur le français)

---

## Résumé : Les 3 tweets essentiels pour la démo

Si vous n'avez le temps que pour 3 tweets :

### 1. Tweet POSITIF évident (Tweet 1)
```
Amazing flight experience! The crew was incredibly friendly and helpful. Best airline I've ever flown with. Highly recommend Air Paradis!
```

### 2. Tweet NÉGATIF évident (Tweet 5)
```
Terrible experience with Air Paradis today. 5-hour delay with no explanation and horrible customer service. Never flying with them again!
```

### 3. Tweet AMBIGU pour montrer les limites (Tweet 9)
```
The flight was okay. Crew was nice but the food could be better. Nothing special, just an average experience with Air Paradis.
```

---

**Bon courage pour votre démonstration !** 🚀✈️
