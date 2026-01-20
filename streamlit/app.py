"""
Interface Streamlit pour tester l'API Air Paradis Sentiment Analysis

Cette application web permet de tester l'API de prédiction de sentiments
de manière interactive et visuelle.

Pour lancer l'application:
    streamlit run streamlit_app.py
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import os
import time
import logging

# Configuration du logging pour Application Insights
logging.basicConfig(level=logging.INFO)

# Configuration de la page
st.set_page_config(
    page_title="Air Paradis - Sentiment Analysis",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration de l'API
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Configuration PostHog Analytics (optionnel)
# Essayer d'abord les secrets Streamlit, puis les variables d'environnement
POSTHOG_API_KEY = ""
POSTHOG_HOST = "https://app.posthog.com"

try:
    # Streamlit Cloud secrets
    if "POSTHOG_API_KEY" in st.secrets:
        POSTHOG_API_KEY = st.secrets["POSTHOG_API_KEY"]
    if "POSTHOG_HOST" in st.secrets:
        POSTHOG_HOST = st.secrets["POSTHOG_HOST"]
except Exception as e:
    pass

# Fallback sur variables d'environnement
if not POSTHOG_API_KEY:
    POSTHOG_API_KEY = os.getenv("POSTHOG_API_KEY", "")

# Flag pour activer/désactiver PostHog
USE_POSTHOG = bool(POSTHOG_API_KEY)

# Logger
logger = logging.getLogger(__name__)

# Importer et configurer PostHog si disponible
posthog_client = None
if USE_POSTHOG:
    try:
        from posthog import Posthog
        posthog_client = Posthog(
            project_api_key=POSTHOG_API_KEY,
            host=POSTHOG_HOST
        )
        logger.info(f"PostHog configuré avec succès (key: {POSTHOG_API_KEY[:10]}...)")
    except ImportError:
        USE_POSTHOG = False
        logger.warning("posthog non installé. Les événements ne seront pas trackés.")
    except Exception as e:
        USE_POSTHOG = False
        logger.error(f"Erreur configuration PostHog: {e}")
else:
    logger.info("PostHog non configuré (pas de clé API)")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 1rem;
    }
    .positive-sentiment {
        background-color: #4CAF50;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .negative-sentiment {
        background-color: #F44336;
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">✈️ Air Paradis - Sentiment Analysis</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Détection de bad buzz en temps réel</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")

    # API URL
    custom_api_url = st.text_input("URL de l'API", value=API_URL)
    if custom_api_url != API_URL:
        API_URL = custom_api_url

    st.divider()

    # Mode
    mode = st.radio(
        "Mode d'analyse",
        ["Tweet unique", "Analyse batch", "Historique"],
        index=0
    )

    st.divider()

    # Status de l'API
    st.subheader("📊 Status de l'API")

    try:
        health_response = requests.get(f"{API_URL}/health", timeout=5)
        if health_response.status_code == 200:
            health_data = health_response.json()
            if health_data["status"] == "healthy":
                st.success("✓ API en ligne")
            else:
                st.warning("⚠️ API dégradée")

            st.metric("Modèle", health_data.get("model_type", "N/A"))
            st.caption(f"Dernière mise à jour: {datetime.now().strftime('%H:%M:%S')}")
        else:
            st.error("✗ API hors ligne")
    except Exception as e:
        st.error("✗ API inaccessible")
        st.caption(f"Erreur: {str(e)}")

    st.divider()

    # Status PostHog
    st.subheader("📊 Analytics")
    if USE_POSTHOG and posthog_client:
        st.success("✓ PostHog connecté")
        st.caption(f"Host: {POSTHOG_HOST}")
    else:
        st.warning("⚠️ PostHog non configuré")
        st.caption("Définir POSTHOG_API_KEY")

    st.divider()

    # Info
    st.caption("Version 1.0.0")
    st.caption("© 2024 Air Paradis")


# Fonction pour prédire un sentiment
def predict_sentiment(text):
    """Appel à l'API pour prédire le sentiment"""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json={"text": text},
            timeout=10
        )

        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erreur {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"


def send_feedback_to_analytics(text, predicted_sentiment, actual_sentiment, confidence, model_type):
    """
    Envoie un feedback utilisateur à PostHog Analytics

    Args:
        text: Le texte du tweet
        predicted_sentiment: Sentiment prédit par le modèle
        actual_sentiment: Sentiment réel indiqué par l'utilisateur
        confidence: Niveau de confiance de la prédiction
        model_type: Type de modèle utilisé
    """
    # Debug info
    logger.info(f"send_feedback_to_analytics called - USE_POSTHOG={USE_POSTHOG}, posthog_client={posthog_client is not None}")

    if USE_POSTHOG and posthog_client:
        try:
            # Générer un ID utilisateur unique basé sur la session
            user_id = st.session_state.get('user_id', f"user_{datetime.now().timestamp()}")
            if 'user_id' not in st.session_state:
                st.session_state.user_id = user_id

            event_data = {
                'feedback_type': 'incorrect_prediction',
                'text_preview': text[:100],
                'text_length': len(text),
                'predicted_sentiment': predicted_sentiment,
                'actual_sentiment': actual_sentiment,
                'confidence': confidence,
                'model_type': model_type,
                'timestamp': datetime.now().isoformat(),
                'source': 'streamlit_interface'
            }

            logger.info(f"Sending event to PostHog: user={user_id}, event=prediction_feedback")

            # Envoyer l'événement à PostHog
            posthog_client.capture(
                distinct_id=user_id,
                event='prediction_feedback',
                properties=event_data
            )

            # IMPORTANT: Forcer l'envoi immédiat des événements
            posthog_client.flush()

            st.success(f"✅ Feedback envoyé à PostHog !")
            logger.info(f"Event sent successfully to PostHog for user {user_id}")
            return True
        except Exception as e:
            st.error(f"❌ Erreur PostHog: {e}")
            logger.error(f"Erreur lors de l'envoi à PostHog: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    else:
        # Mode debug local
        st.warning(f"⚠️ PostHog non configuré (USE_POSTHOG={USE_POSTHOG})")
        return False


def predict_batch(tweets):
    """Appel à l'API pour prédire plusieurs tweets"""
    try:
        response = requests.post(
            f"{API_URL}/predict/batch",
            json={"tweets": tweets},
            timeout=30
        )

        if response.status_code == 200:
            return response.json(), None
        else:
            return None, f"Erreur {response.status_code}: {response.text}"
    except Exception as e:
        return None, f"Erreur de connexion: {str(e)}"


# Mode: Tweet unique
if mode == "Tweet unique":
    st.header("🐦 Analyse d'un tweet unique")

    # Zone de texte
    tweet_text = st.text_area(
        "Entrez le texte du tweet à analyser:",
        placeholder="Exemple: This flight was amazing! Best experience ever!",
        height=100,
        max_chars=280
    )

    # Compteur de caractères
    char_count = len(tweet_text)
    col1, col2 = st.columns([3, 1])
    with col2:
        if char_count > 280:
            st.error(f"⚠️ {char_count}/280 caractères")
        else:
            st.caption(f"{char_count}/280 caractères")

    # Bouton de prédiction
    if st.button("🔍 Analyser le sentiment", type="primary", use_container_width=True):
        if not tweet_text.strip():
            st.warning("⚠️ Veuillez entrer un texte à analyser")
        else:
            with st.spinner("Analyse en cours..."):
                result, error = predict_sentiment(tweet_text)

            if error:
                st.error(f"❌ {error}")
            else:
                # Stocker le résultat dans session_state pour persistance
                st.session_state.last_result = result
                st.session_state.last_tweet = tweet_text
                st.session_state.show_correction = False
                st.session_state.feedback_sent = False  # Reset feedback pour nouvelle analyse

    # Afficher le résultat s'il existe dans session_state
    if 'last_result' in st.session_state and st.session_state.last_result:
        result = st.session_state.last_result
        tweet_text = st.session_state.last_tweet

        # Affichage du résultat
        st.success("✅ Analyse terminée")

        # Sentiment principal
        sentiment_label = result["sentiment_label"]
        confidence = result["confidence"]

        if sentiment_label == "Positif":
            st.markdown(
                f'<div class="positive-sentiment">😊 SENTIMENT POSITIF<br>'
                f'Confiance: {confidence:.1%}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="negative-sentiment">😞 SENTIMENT NÉGATIF<br>'
                f'Confiance: {confidence:.1%}</div>',
                unsafe_allow_html=True
            )

        st.divider()

        # Détails
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Sentiment",
                sentiment_label,
                delta=f"{confidence:.1%}" if sentiment_label == "Positif" else f"-{confidence:.1%}"
            )

        with col2:
            st.metric(
                "Confiance",
                f"{confidence:.1%}"
            )

        with col3:
            st.metric(
                "Modèle",
                result["model_type"].upper()
            )

        # Graphique de probabilités
        st.subheader("📊 Distribution des probabilités")

        probabilities = result["probabilities"]
        fig = go.Figure(data=[
            go.Bar(
                x=["Négatif", "Positif"],
                y=[probabilities["negative"], probabilities["positive"]],
                marker_color=["#F44336", "#4CAF50"],
                text=[f"{probabilities['negative']:.1%}", f"{probabilities['positive']:.1%}"],
                textposition="auto"
            )
        ])

        fig.update_layout(
            title="Probabilités de classification",
            xaxis_title="Sentiment",
            yaxis_title="Probabilité",
            yaxis_range=[0, 1],
            height=400
        )

        st.plotly_chart(fig, use_container_width=True)

        # JSON brut
        with st.expander("🔍 Voir la réponse JSON complète"):
            st.json(result)

        # Validation utilisateur
        st.divider()
        st.subheader("🗳️ Cette prédiction est-elle correcte ?")

        # État du feedback
        if 'feedback_sent' not in st.session_state:
            st.session_state.feedback_sent = False

        if not st.session_state.feedback_sent:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("👍 Oui, c'est correct", type="primary", use_container_width=True, key="correct"):
                    st.session_state.feedback_sent = True
                    st.success("Merci pour votre validation ! 😊")

            with col2:
                if st.button("👎 Non, c'est faux", type="secondary", use_container_width=True, key="incorrect"):
                    st.session_state.show_correction = True

            # Si l'utilisateur a cliqué "Non", afficher les options de correction
            if st.session_state.get('show_correction', False):
                st.markdown("---")
                st.markdown("**Quel était le vrai sentiment ?**")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("😊 C'était POSITIF", use_container_width=True, key="correct_positive"):
                        sent = send_feedback_to_analytics(
                            text=tweet_text,
                            predicted_sentiment=sentiment_label,
                            actual_sentiment="Positif",
                            confidence=confidence,
                            model_type=result["model_type"]
                        )
                        st.session_state.show_correction = False
                        st.session_state.feedback_sent = True

                with col2:
                    if st.button("😞 C'était NÉGATIF", use_container_width=True, key="correct_negative"):
                        sent = send_feedback_to_analytics(
                            text=tweet_text,
                            predicted_sentiment=sentiment_label,
                            actual_sentiment="Négatif",
                            confidence=confidence,
                            model_type=result["model_type"]
                        )
                        st.session_state.show_correction = False
                        st.session_state.feedback_sent = True
        else:
            st.success("✅ Merci pour votre feedback !")


# Mode: Analyse batch
elif mode == "Analyse batch":
    st.header("📊 Analyse batch de tweets")

    st.info("💡 Analysez jusqu'à 100 tweets simultanément")

    # Zone de texte pour plusieurs tweets
    batch_text = st.text_area(
        "Entrez les tweets (un par ligne):",
        placeholder="Great service!\nBad experience\nAmazing quality!",
        height=200
    )

    # Ou upload d'un fichier CSV
    st.markdown("**Ou importez un fichier CSV:**")
    uploaded_file = st.file_uploader("Choisir un fichier CSV", type=["csv"])

    tweets_list = []

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "text" in df.columns:
            tweets_list = df["text"].tolist()
            st.success(f"✓ {len(tweets_list)} tweets chargés depuis le fichier")
        else:
            st.error("❌ Le fichier doit contenir une colonne 'text'")
    elif batch_text.strip():
        tweets_list = [line.strip() for line in batch_text.split("\n") if line.strip()]

    # Affichage du nombre de tweets
    if tweets_list:
        st.caption(f"📝 {len(tweets_list)} tweet(s) à analyser")

    # Bouton d'analyse
    if st.button("🔍 Analyser tous les tweets", type="primary", use_container_width=True):
        if not tweets_list:
            st.warning("⚠️ Veuillez entrer des tweets à analyser")
        elif len(tweets_list) > 100:
            st.error("❌ Maximum 100 tweets par analyse")
        else:
            with st.spinner(f"Analyse de {len(tweets_list)} tweets en cours..."):
                start_time = time.time()
                result, error = predict_batch(tweets_list)
                elapsed_time = time.time() - start_time

            if error:
                st.error(f"❌ {error}")
            else:
                st.success(f"✅ Analyse terminée en {elapsed_time:.2f}s")

                # Statistiques globales
                predictions = result["predictions"]
                positive_count = sum(1 for p in predictions if p["sentiment_label"] == "Positif")
                negative_count = len(predictions) - positive_count

                # Métriques
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total", len(predictions))

                with col2:
                    st.metric("Positifs", positive_count, delta=f"{positive_count/len(predictions):.0%}")

                with col3:
                    st.metric("Négatifs", negative_count, delta=f"-{negative_count/len(predictions):.0%}")

                with col4:
                    avg_confidence = sum(p["confidence"] for p in predictions) / len(predictions)
                    st.metric("Confiance moy.", f"{avg_confidence:.1%}")

                st.divider()

                # Graphique de distribution
                col1, col2 = st.columns(2)

                with col1:
                    # Pie chart
                    fig_pie = go.Figure(data=[go.Pie(
                        labels=["Positif", "Négatif"],
                        values=[positive_count, negative_count],
                        marker_colors=["#4CAF50", "#F44336"],
                        hole=0.3
                    )])
                    fig_pie.update_layout(title="Distribution des sentiments", height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)

                with col2:
                    # Histogram de confiance
                    confidences = [p["confidence"] for p in predictions]
                    fig_hist = px.histogram(
                        x=confidences,
                        nbins=20,
                        title="Distribution des niveaux de confiance",
                        labels={"x": "Confiance", "y": "Nombre de tweets"}
                    )
                    fig_hist.update_layout(height=400)
                    st.plotly_chart(fig_hist, use_container_width=True)

                # Tableau des résultats
                st.subheader("📋 Détails des prédictions")

                df_results = pd.DataFrame([
                    {
                        "Tweet": p["text"][:50] + "..." if len(p["text"]) > 50 else p["text"],
                        "Sentiment": p["sentiment_label"],
                        "Confiance": f"{p['confidence']:.1%}",
                        "Prob. Positif": f"{p['probabilities']['positive']:.1%}",
                        "Prob. Négatif": f"{p['probabilities']['negative']:.1%}"
                    }
                    for p in predictions
                ])

                # Colorier selon le sentiment
                def highlight_sentiment(row):
                    if row["Sentiment"] == "Positif":
                        return ["background-color: #C8E6C9"] * len(row)
                    else:
                        return ["background-color: #FFCDD2"] * len(row)

                st.dataframe(
                    df_results.style.apply(highlight_sentiment, axis=1),
                    use_container_width=True,
                    height=400
                )

                # Bouton de téléchargement
                csv = df_results.to_csv(index=False)
                st.download_button(
                    label="📥 Télécharger les résultats (CSV)",
                    data=csv,
                    file_name=f"sentiment_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )


# Mode: Historique
elif mode == "Historique":
    st.header("📈 Historique des analyses")

    st.info("🚧 Fonctionnalité en cours de développement")

    st.markdown("""
    Cette section permettra de visualiser:
    - L'historique des analyses effectuées
    - Les tendances de sentiments au fil du temps
    - Les alertes de bad buzz détectées
    - Les statistiques d'utilisation de l'API
    """)

    # Exemple de graphique temporel
    st.subheader("Tendance des sentiments (exemple)")

    # Données d'exemple
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    import numpy as np
    positive_trend = 50 + np.random.randn(len(dates)).cumsum() * 2
    negative_trend = 50 - np.random.randn(len(dates)).cumsum() * 2

    df_trend = pd.DataFrame({
        "Date": dates,
        "Positif": positive_trend,
        "Négatif": negative_trend
    })

    fig_trend = px.line(
        df_trend,
        x="Date",
        y=["Positif", "Négatif"],
        title="Évolution des sentiments au fil du temps",
        labels={"value": "Nombre de tweets", "variable": "Sentiment"},
        color_discrete_map={"Positif": "#4CAF50", "Négatif": "#F44336"}
    )

    st.plotly_chart(fig_trend, use_container_width=True)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem 0;'>
    <p>Air Paradis - Sentiment Analysis API v1.0.0</p>
    <p>Développé avec ❤️ pour OpenClassrooms Projet 7</p>
    <p>
        <a href='/docs' target='_blank'>Documentation API</a> •
        <a href='https://github.com' target='_blank'>GitHub</a>
    </p>
</div>
""", unsafe_allow_html=True)
