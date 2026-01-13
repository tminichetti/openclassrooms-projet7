# Interface Streamlit - Air Paradis Sentiment Analysis

Interface utilisateur pour tester l'API de sentiment analysis avec système de validation.

## Déploiement sur Streamlit Cloud

1. **Repository** : `ton-username/openclassrooms-projet7`
2. **Branch** : `main`
3. **Main file path** : `streamlit/app.py`
4. **App URL** : Choisir un nom (ex: `airparadis-sentiment`)

## Configuration des secrets

Dans Streamlit Cloud → Settings → Secrets :

```toml
API_URL = "https://openclassrooms-projet7-5e5ebd15aa21.herokuapp.com"

# PostHog Analytics (optionnel - pour tracking des feedbacks)
POSTHOG_API_KEY = "phx_2u4dbbg075A8yzkwoEQgL0RyASH66ppxg0jzAqRNLgZauYV"
POSTHOG_HOST = "https://app.posthog.com"
```

## Test local

```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
```

## Fonctionnalités

- Analyse de sentiment (tweet unique)
- Analyse batch (CSV)
- Validation utilisateur (correct/incorrect)
- Feedback vers PostHog Analytics (optionnel)
- Visualisations et statistiques

## Analytics avec PostHog

L'interface envoie automatiquement les événements suivants à PostHog :
- **prediction_feedback** : Quand un utilisateur corrige une prédiction incorrecte
- Propriétés trackées : sentiment prédit, sentiment réel, confiance, longueur du texte, type de modèle

Vous pouvez visualiser ces données dans PostHog pour :
- Identifier les erreurs fréquentes du modèle
- Analyser la confiance des prédictions incorrectes
- Suivre l'évolution de la qualité du modèle
