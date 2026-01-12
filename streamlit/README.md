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
API_URL = "https://ton-api.herokuapp.com"
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
- Feedback vers Azure Application Insights (optionnel)
- Visualisations et statistiques
