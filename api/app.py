"""
API FastAPI pour la prédiction de sentiments de tweets - Air Paradis

Cette API permet de prédire le sentiment (positif/négatif) de tweets pour détecter
le bad buzz en temps réel.

Endpoints:
    - GET /: Page d'accueil avec informations API
    - GET /health: Health check
    - POST /predict: Prédiction de sentiment
    - POST /predict/batch: Prédiction batch
    - GET /models: Liste des modèles disponibles
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict
import logging
from datetime import datetime
import os
import joblib
import numpy as np

# Imports conditionnels pour les modèles lourds (uniquement si nécessaire)
try:
    import tensorflow as tf
    from transformers import BertTokenizer, TFBertForSequenceClassification
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning("TensorFlow/Transformers non disponibles. Seul le modèle logistique sera utilisable.")

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Air Paradis - Sentiment Analysis API",
    description="API de prédiction de sentiments pour la détection de bad buzz",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis d'autres domaines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales pour les modèles
MODEL_TYPE = os.getenv("MODEL_TYPE", "logistic")  # bert, lstm, cnn, logistic
MODEL_PATH = os.getenv("MODEL_PATH", "./models/logistic_regression_model.pkl")
model = None
tokenizer = None
vectorizer = None

# Configuration
MAX_LENGTH = 128
SENTIMENT_LABELS = {0: "Négatif", 1: "Positif"}


# Modèles Pydantic pour la validation
class TweetInput(BaseModel):
    """Modèle pour un tweet unique"""
    text: str = Field(..., min_length=1, max_length=280, description="Texte du tweet")

    @validator('text')
    def validate_text(cls, v):
        if not v.strip():
            raise ValueError("Le texte ne peut pas être vide")
        return v.strip()


class TweetBatchInput(BaseModel):
    """Modèle pour plusieurs tweets"""
    tweets: List[str] = Field(..., min_items=1, max_items=100, description="Liste de tweets")

    @validator('tweets')
    def validate_tweets(cls, v):
        if not v:
            raise ValueError("La liste ne peut pas être vide")
        if len(v) > 100:
            raise ValueError("Maximum 100 tweets par requête")
        return [tweet.strip() for tweet in v if tweet.strip()]


class PredictionOutput(BaseModel):
    """Modèle de sortie pour une prédiction"""
    text: str
    sentiment: str
    sentiment_label: str
    confidence: float
    probabilities: Dict[str, float]
    timestamp: str
    model_type: str


class BatchPredictionOutput(BaseModel):
    """Modèle de sortie pour des prédictions batch"""
    predictions: List[PredictionOutput]
    count: int
    model_type: str
    timestamp: str


class HealthResponse(BaseModel):
    """Modèle de sortie pour le health check"""
    status: str
    model_loaded: bool
    model_type: str
    timestamp: str


class ModelInfo(BaseModel):
    """Information sur les modèles disponibles"""
    available_models: List[str]
    current_model: str
    model_path: str


def load_bert_model():
    """Charge le modèle BERT et son tokenizer"""
    global model, tokenizer

    if not TF_AVAILABLE:
        logger.error("TensorFlow/Transformers non installés. Impossible de charger BERT.")
        return False

    try:
        logger.info(f"Chargement du modèle BERT depuis {MODEL_PATH}")
        model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)
        tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
        logger.info("Modèle BERT chargé avec succès")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle BERT: {e}")
        return False


def load_dl_model(model_path: str):
    """Charge un modèle Deep Learning (LSTM/CNN)"""
    global model, vectorizer, tokenizer

    if not TF_AVAILABLE:
        logger.error("TensorFlow non installé. Impossible de charger le modèle Deep Learning.")
        return False

    try:
        logger.info(f"Chargement du modèle DL depuis {model_path}")
        model = tf.keras.models.load_model(model_path)

        # Charger le tokenizer Keras associé
        tokenizer_path = model_path.replace('.h5', '_tokenizer.pkl')
        if os.path.exists(tokenizer_path):
            tokenizer = joblib.load(tokenizer_path)

        logger.info("Modèle DL chargé avec succès")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle DL: {e}")
        return False


def load_logistic_model(model_path: str):
    """Charge le modèle de régression logistique"""
    global model, vectorizer
    try:
        logger.info(f"Chargement du modèle logistique depuis {model_path}")
        logger.info(f"Chemin absolu: {os.path.abspath(model_path)}")
        logger.info(f"Fichier existe: {os.path.exists(model_path)}")

        model = joblib.load(model_path)
        logger.info(f"Modèle chargé: {type(model)}")

        # Charger le vectorizer TF-IDF associé
        # Chercher d'abord dans le même dossier
        base_dir = os.path.dirname(model_path)
        logger.info(f"Base dir: {base_dir}")

        vectorizer_path = os.path.join(base_dir, 'tfidf_vectorizer.pkl')
        logger.info(f"Tentative 1 - Chemin vectorizer: {vectorizer_path}")
        logger.info(f"Tentative 1 - Existe: {os.path.exists(vectorizer_path)}")

        if not os.path.exists(vectorizer_path):
            # Fallback sur l'ancien chemin
            vectorizer_path = model_path.replace('logistic_regression_model.pkl', 'tfidf_vectorizer.pkl')
            logger.info(f"Tentative 2 - Chemin vectorizer: {vectorizer_path}")
            logger.info(f"Tentative 2 - Existe: {os.path.exists(vectorizer_path)}")

        if os.path.exists(vectorizer_path):
            vectorizer = joblib.load(vectorizer_path)
            logger.info(f"Vectorizer chargé depuis {vectorizer_path}: {type(vectorizer)}")
        else:
            logger.error(f"Vectorizer non trouvé: {vectorizer_path}")
            # Lister les fichiers dans le dossier models
            if os.path.exists(base_dir):
                logger.info(f"Contenu de {base_dir}: {os.listdir(base_dir)}")
            return False

        logger.info("Modèle logistique chargé avec succès")
        return True
    except Exception as e:
        logger.error(f"Erreur lors du chargement du modèle logistique: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False


def predict_bert(text: str) -> tuple:
    """
    Prédiction avec BERT

    Returns:
        (predicted_class, confidence, probabilities)
    """
    # Tokenisation
    encoding = tokenizer(
        text,
        truncation=True,
        padding='max_length',
        max_length=MAX_LENGTH,
        return_tensors='tf'
    )

    # Prédiction
    outputs = model(encoding)
    logits = outputs.logits
    probabilities = tf.nn.softmax(logits, axis=1).numpy()[0]

    predicted_class = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_class])

    return predicted_class, confidence, {
        "negative": float(probabilities[0]),
        "positive": float(probabilities[1])
    }


def predict_dl(text: str) -> tuple:
    """
    Prédiction avec modèle Deep Learning (LSTM/CNN)

    Returns:
        (predicted_class, confidence, probabilities)
    """
    # Tokenisation avec Keras Tokenizer
    sequence = tokenizer.texts_to_sequences([text])
    padded = tf.keras.preprocessing.sequence.pad_sequences(
        sequence,
        maxlen=MAX_LENGTH,
        padding='post'
    )

    # Prédiction
    prediction = model.predict(padded, verbose=0)[0]

    if len(prediction) == 2:
        probabilities = prediction
    else:
        # Si sortie unique (sigmoid)
        prob_positive = float(prediction[0])
        probabilities = [1 - prob_positive, prob_positive]

    predicted_class = int(np.argmax(probabilities))
    confidence = float(probabilities[predicted_class])

    return predicted_class, confidence, {
        "negative": float(probabilities[0]),
        "positive": float(probabilities[1])
    }


def predict_logistic(text: str) -> tuple:
    """
    Prédiction avec régression logistique

    Returns:
        (predicted_class, confidence, probabilities)
    """
    # Vectorisation TF-IDF
    text_vectorized = vectorizer.transform([text])

    # Prédiction
    predicted_class = int(model.predict(text_vectorized)[0])
    probabilities = model.predict_proba(text_vectorized)[0]
    confidence = float(probabilities[predicted_class])

    return predicted_class, confidence, {
        "negative": float(probabilities[0]),
        "positive": float(probabilities[1])
    }


@app.on_event("startup")
async def startup_event():
    """Charge le modèle au démarrage de l'API"""
    logger.info("Démarrage de l'API Air Paradis Sentiment Analysis")

    # Chargement du modèle selon le type
    if MODEL_TYPE == "bert":
        success = load_bert_model()
    elif MODEL_TYPE in ["lstm", "cnn"]:
        success = load_dl_model(MODEL_PATH)
    elif MODEL_TYPE == "logistic":
        success = load_logistic_model(MODEL_PATH)
    else:
        logger.error(f"Type de modèle non reconnu: {MODEL_TYPE}")
        success = False

    if not success:
        logger.warning("Impossible de charger le modèle au démarrage")
    else:
        logger.info(f"Modèle {MODEL_TYPE} chargé et prêt")


@app.get("/", response_model=Dict)
async def root():
    """
    Page d'accueil de l'API avec informations de base
    """
    return {
        "message": "Air Paradis - Sentiment Analysis API",
        "version": "1.0.0",
        "description": "API de prédiction de sentiments pour la détection de bad buzz",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "predict_batch": "/predict/batch (POST)",
            "models": "/models (GET)",
            "documentation": "/docs"
        },
        "model_type": MODEL_TYPE,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check pour vérifier que l'API fonctionne
    """
    model_loaded = model is not None

    # Log supplémentaire pour debug
    logger.info(f"Health check: model={model is not None}, vectorizer={vectorizer is not None}, tokenizer={tokenizer is not None}")

    return HealthResponse(
        status="healthy" if model_loaded else "degraded",
        model_loaded=model_loaded,
        model_type=MODEL_TYPE,
        timestamp=datetime.now().isoformat()
    )


@app.get("/models", response_model=ModelInfo)
async def get_models():
    """
    Retourne les informations sur les modèles disponibles
    """
    return ModelInfo(
        available_models=["bert", "lstm", "cnn", "logistic"],
        current_model=MODEL_TYPE,
        model_path=MODEL_PATH
    )


@app.get("/debug/files")
async def debug_files():
    """
    Endpoint de debug pour vérifier les fichiers présents
    """
    import glob
    import sklearn

    vectorizer_info = {}
    if vectorizer is not None:
        vectorizer_info = {
            "type": str(type(vectorizer)),
            "has_idf": hasattr(vectorizer, "idf_"),
            "has_vocabulary": hasattr(vectorizer, "vocabulary_"),
            "vocabulary_size": len(vectorizer.vocabulary_) if hasattr(vectorizer, "vocabulary_") else 0,
        }

    return {
        "cwd": os.getcwd(),
        "sklearn_version": sklearn.__version__,
        "model_path": MODEL_PATH,
        "model_path_exists": os.path.exists(MODEL_PATH),
        "models_dir": os.path.exists("./models"),
        "models_files": glob.glob("./models/*") if os.path.exists("./models") else [],
        "api_models_dir": os.path.exists("api/models"),
        "api_models_files": glob.glob("api/models/*") if os.path.exists("api/models") else [],
        "model_loaded": model is not None,
        "vectorizer_loaded": vectorizer is not None,
        "vectorizer_info": vectorizer_info,
    }


@app.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK)
async def predict_sentiment(tweet: TweetInput):
    """
    Prédit le sentiment d'un tweet unique

    Args:
        tweet: Objet contenant le texte du tweet

    Returns:
        Prédiction avec sentiment, confiance et probabilités

    Raises:
        HTTPException 503: Si le modèle n'est pas chargé
        HTTPException 500: Si erreur lors de la prédiction
    """
    # Vérifier que le modèle est chargé
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé. Veuillez contacter l'administrateur."
        )

    try:
        logger.info(f"Prédiction pour: {tweet.text[:50]}...")

        # Prédiction selon le type de modèle
        if MODEL_TYPE == "bert":
            predicted_class, confidence, probabilities = predict_bert(tweet.text)
        elif MODEL_TYPE in ["lstm", "cnn"]:
            predicted_class, confidence, probabilities = predict_dl(tweet.text)
        elif MODEL_TYPE == "logistic":
            predicted_class, confidence, probabilities = predict_logistic(tweet.text)
        else:
            raise ValueError(f"Type de modèle non supporté: {MODEL_TYPE}")

        sentiment_label = SENTIMENT_LABELS[predicted_class]

        logger.info(f"Prédiction: {sentiment_label} (confiance: {confidence:.2%})")

        return PredictionOutput(
            text=tweet.text,
            sentiment=str(predicted_class),
            sentiment_label=sentiment_label,
            confidence=confidence,
            probabilities=probabilities,
            timestamp=datetime.now().isoformat(),
            model_type=MODEL_TYPE
        )

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction: {str(e)}"
        )


@app.post("/predict/batch", response_model=BatchPredictionOutput, status_code=status.HTTP_200_OK)
async def predict_batch(batch: TweetBatchInput):
    """
    Prédit le sentiment de plusieurs tweets

    Args:
        batch: Objet contenant une liste de tweets

    Returns:
        Liste de prédictions

    Raises:
        HTTPException 503: Si le modèle n'est pas chargé
        HTTPException 500: Si erreur lors de la prédiction
    """
    # Vérifier que le modèle est chargé
    if model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modèle non chargé. Veuillez contacter l'administrateur."
        )

    try:
        logger.info(f"Prédiction batch de {len(batch.tweets)} tweets")

        predictions = []
        for tweet_text in batch.tweets:
            # Prédiction selon le type de modèle
            if MODEL_TYPE == "bert":
                predicted_class, confidence, probabilities = predict_bert(tweet_text)
            elif MODEL_TYPE in ["lstm", "cnn"]:
                predicted_class, confidence, probabilities = predict_dl(tweet_text)
            elif MODEL_TYPE == "logistic":
                predicted_class, confidence, probabilities = predict_logistic(tweet_text)
            else:
                raise ValueError(f"Type de modèle non supporté: {MODEL_TYPE}")

            sentiment_label = SENTIMENT_LABELS[predicted_class]

            predictions.append(PredictionOutput(
                text=tweet_text,
                sentiment=str(predicted_class),
                sentiment_label=sentiment_label,
                confidence=confidence,
                probabilities=probabilities,
                timestamp=datetime.now().isoformat(),
                model_type=MODEL_TYPE
            ))

        logger.info(f"Prédictions batch terminées: {len(predictions)} résultats")

        return BatchPredictionOutput(
            predictions=predictions,
            count=len(predictions),
            model_type=MODEL_TYPE,
            timestamp=datetime.now().isoformat()
        )

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction batch: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la prédiction batch: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    # Démarrage du serveur
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
