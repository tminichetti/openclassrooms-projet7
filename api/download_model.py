"""
Script pour télécharger et préparer les modèles pour Heroku

Ce script télécharge les modèles nécessaires depuis Hugging Face ou Google Drive
au démarrage de l'application sur Heroku.
"""

import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_bert_model():
    """
    Télécharge le modèle BERT pré-entraîné pour l'analyse de sentiments

    Utilise un modèle BERT fine-tuné pour l'analyse de sentiments de tweets
    depuis Hugging Face Hub
    """
    try:
        from transformers import BertTokenizer, TFBertForSequenceClassification

        model_name = os.getenv("BERT_MODEL_NAME", "nlptown/bert-base-multilingual-uncased-sentiment")
        models_dir = Path("./models")
        bert_dir = models_dir / "bert_sentiment_model"

        # Créer le dossier models s'il n'existe pas
        models_dir.mkdir(exist_ok=True)
        bert_dir.mkdir(exist_ok=True)

        logger.info(f"Téléchargement du modèle BERT depuis Hugging Face: {model_name}")

        # Télécharger et sauvegarder le tokenizer
        tokenizer = BertTokenizer.from_pretrained(model_name)
        tokenizer.save_pretrained(bert_dir)
        logger.info(f"Tokenizer sauvegardé dans {bert_dir}")

        # Télécharger et sauvegarder le modèle
        # Note: On utilise un modèle pré-entraîné car le vôtre est trop gros
        # En production, vous devriez uploader votre modèle sur Hugging Face Hub
        model = TFBertForSequenceClassification.from_pretrained(
            model_name,
            num_labels=2  # Positif/Négatif
        )
        model.save_pretrained(bert_dir)
        logger.info(f"Modèle BERT sauvegardé dans {bert_dir}")

        return True

    except Exception as e:
        logger.error(f"Erreur lors du téléchargement du modèle BERT: {e}")
        return False


def download_logistic_model():
    """
    Pour le modèle logistique, on peut soit:
    1. L'inclure dans Git (il est léger ~80KB)
    2. Le télécharger depuis un stockage externe

    Pour l'instant, on suppose qu'il est déjà inclus dans le repo
    """
    models_dir = Path("./models")
    logistic_model_path = models_dir / "logistic_regression_model.pkl"
    vectorizer_path = models_dir / "tfidf_vectorizer.pkl"

    if logistic_model_path.exists() and vectorizer_path.exists():
        logger.info("Modèle logistique déjà présent")
        return True
    else:
        logger.warning("Modèle logistique non trouvé. Assurez-vous qu'il est dans le repo Git.")
        return False


def setup_models():
    """
    Configure les modèles selon le type spécifié dans les variables d'environnement
    """
    model_type = os.getenv("MODEL_TYPE", "logistic")

    logger.info(f"Configuration des modèles pour le type: {model_type}")

    if model_type == "bert":
        return download_bert_model()
    elif model_type == "logistic":
        return download_logistic_model()
    else:
        logger.warning(f"Type de modèle non reconnu: {model_type}")
        return False


if __name__ == "__main__":
    """
    Exécuter ce script avant de démarrer l'application
    """
    logger.info("Démarrage du téléchargement des modèles...")
    success = setup_models()

    if success:
        logger.info("✓ Modèles configurés avec succès")
    else:
        logger.error("✗ Erreur lors de la configuration des modèles")
        exit(1)
