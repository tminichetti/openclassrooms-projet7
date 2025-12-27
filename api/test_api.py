"""
Tests unitaires pour l'API de prédiction de sentiments

Ces tests vérifient le bon fonctionnement de tous les endpoints de l'API.

Pour exécuter les tests:
    pytest test_api.py -v
    pytest test_api.py -v --cov=app --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch, MagicMock
import numpy as np
import tensorflow as tf
from datetime import datetime

# Import de l'application
from app import app, load_bert_model, predict_bert, predict_logistic

# Client de test
client = TestClient(app)


# Fixtures
@pytest.fixture
def mock_bert_model():
    """Mock du modèle BERT"""
    mock_model = Mock()
    mock_outputs = Mock()
    mock_outputs.logits = tf.constant([[0.2, 0.8]])  # Prédiction positive
    mock_model.return_value = mock_outputs
    return mock_model


@pytest.fixture
def mock_bert_tokenizer():
    """Mock du tokenizer BERT"""
    mock_tokenizer = Mock()
    mock_tokenizer.return_value = {
        'input_ids': tf.constant([[101, 2023, 2003, 1037, 3231, 102]]),
        'attention_mask': tf.constant([[1, 1, 1, 1, 1, 1]])
    }
    return mock_tokenizer


@pytest.fixture
def mock_logistic_model():
    """Mock du modèle logistique"""
    mock_model = Mock()
    mock_model.predict.return_value = np.array([1])  # Prédiction positive
    mock_model.predict_proba.return_value = np.array([[0.3, 0.7]])
    return mock_model


@pytest.fixture
def mock_vectorizer():
    """Mock du vectorizer TF-IDF"""
    mock_vec = Mock()
    mock_vec.transform.return_value = Mock()
    return mock_vec


@pytest.fixture
def sample_tweet():
    """Tweet exemple pour les tests"""
    return {"text": "This is an amazing product! I love it!"}


@pytest.fixture
def sample_negative_tweet():
    """Tweet négatif exemple"""
    return {"text": "Terrible experience, worst service ever!"}


@pytest.fixture
def sample_batch():
    """Batch de tweets pour les tests"""
    return {
        "tweets": [
            "Great service!",
            "Bad experience",
            "Amazing quality!"
        ]
    }


# Tests des endpoints de base
class TestBasicEndpoints:
    """Tests des endpoints de base (root, health, models)"""

    def test_root_endpoint(self):
        """Test du endpoint racine"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "version" in data
        assert "endpoints" in data
        assert data["message"] == "Air Paradis - Sentiment Analysis API"
        assert data["version"] == "1.0.0"

    def test_health_check(self):
        """Test du health check"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert "status" in data
        assert "model_loaded" in data
        assert "model_type" in data
        assert "timestamp" in data
        assert data["status"] in ["healthy", "degraded"]

    def test_get_models_info(self):
        """Test du endpoint d'information sur les modèles"""
        response = client.get("/models")

        assert response.status_code == 200
        data = response.json()

        assert "available_models" in data
        assert "current_model" in data
        assert "model_path" in data
        assert isinstance(data["available_models"], list)
        assert len(data["available_models"]) > 0


# Tests de l'endpoint de prédiction simple
class TestPredictEndpoint:
    """Tests de l'endpoint /predict"""

    @patch('app.model')
    @patch('app.tokenizer')
    def test_predict_positive_sentiment(self, mock_tokenizer, mock_model, sample_tweet):
        """Test de prédiction d'un sentiment positif"""
        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 2003, 102]]),
            'attention_mask': tf.constant([[1, 1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.2, 0.8]])
        mock_model.return_value = mock_outputs

        # Requête
        response = client.post("/predict", json=sample_tweet)

        # Vérifications
        assert response.status_code == 200
        data = response.json()

        assert "text" in data
        assert "sentiment" in data
        assert "sentiment_label" in data
        assert "confidence" in data
        assert "probabilities" in data
        assert "timestamp" in data
        assert "model_type" in data

        assert data["text"] == sample_tweet["text"]
        assert data["sentiment_label"] in ["Positif", "Négatif"]
        assert 0 <= data["confidence"] <= 1

    @patch('app.model')
    @patch('app.tokenizer')
    def test_predict_negative_sentiment(self, mock_tokenizer, mock_model, sample_negative_tweet):
        """Test de prédiction d'un sentiment négatif"""
        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 2003, 102]]),
            'attention_mask': tf.constant([[1, 1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.9, 0.1]])  # Négatif
        mock_model.return_value = mock_outputs

        # Requête
        response = client.post("/predict", json=sample_negative_tweet)

        # Vérifications
        assert response.status_code == 200
        data = response.json()

        assert data["text"] == sample_negative_tweet["text"]
        assert "sentiment_label" in data

    def test_predict_empty_text(self):
        """Test avec un texte vide"""
        response = client.post("/predict", json={"text": ""})

        assert response.status_code == 422  # Validation error

    def test_predict_text_too_long(self):
        """Test avec un texte trop long (>280 caractères)"""
        long_text = "a" * 281
        response = client.post("/predict", json={"text": long_text})

        assert response.status_code == 422  # Validation error

    def test_predict_invalid_json(self):
        """Test avec un JSON invalide"""
        response = client.post("/predict", json={"wrong_field": "test"})

        assert response.status_code == 422  # Validation error

    @patch('app.model', None)
    def test_predict_model_not_loaded(self, sample_tweet):
        """Test quand le modèle n'est pas chargé"""
        response = client.post("/predict", json=sample_tweet)

        assert response.status_code == 503  # Service unavailable
        assert "Modèle non chargé" in response.json()["detail"]


# Tests de l'endpoint de prédiction batch
class TestPredictBatchEndpoint:
    """Tests de l'endpoint /predict/batch"""

    @patch('app.model')
    @patch('app.tokenizer')
    def test_predict_batch_success(self, mock_tokenizer, mock_model, sample_batch):
        """Test de prédiction batch réussie"""
        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 102]]),
            'attention_mask': tf.constant([[1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.3, 0.7]])
        mock_model.return_value = mock_outputs

        # Requête
        response = client.post("/predict/batch", json=sample_batch)

        # Vérifications
        assert response.status_code == 200
        data = response.json()

        assert "predictions" in data
        assert "count" in data
        assert "model_type" in data
        assert "timestamp" in data

        assert data["count"] == len(sample_batch["tweets"])
        assert len(data["predictions"]) == len(sample_batch["tweets"])

        # Vérifier chaque prédiction
        for pred in data["predictions"]:
            assert "text" in pred
            assert "sentiment" in pred
            assert "sentiment_label" in pred
            assert "confidence" in pred
            assert "probabilities" in pred

    def test_predict_batch_empty_list(self):
        """Test avec une liste vide"""
        response = client.post("/predict/batch", json={"tweets": []})

        assert response.status_code == 422  # Validation error

    def test_predict_batch_too_many(self):
        """Test avec trop de tweets (>100)"""
        too_many_tweets = {"tweets": ["test"] * 101}
        response = client.post("/predict/batch", json=too_many_tweets)

        assert response.status_code == 422  # Validation error

    @patch('app.model', None)
    def test_predict_batch_model_not_loaded(self, sample_batch):
        """Test batch quand le modèle n'est pas chargé"""
        response = client.post("/predict/batch", json=sample_batch)

        assert response.status_code == 503  # Service unavailable


# Tests des fonctions de prédiction
class TestPredictionFunctions:
    """Tests des fonctions de prédiction internes"""

    @patch('app.model')
    @patch('app.tokenizer')
    def test_predict_bert_function(self, mock_tokenizer, mock_model):
        """Test de la fonction predict_bert"""
        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 102]]),
            'attention_mask': tf.constant([[1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.2, 0.8]])
        mock_model.return_value = mock_outputs

        # Test
        predicted_class, confidence, probabilities = predict_bert("test text")

        # Vérifications
        assert predicted_class in [0, 1]
        assert 0 <= confidence <= 1
        assert "negative" in probabilities
        assert "positive" in probabilities
        assert abs(probabilities["negative"] + probabilities["positive"] - 1.0) < 0.01

    @patch('app.model')
    @patch('app.vectorizer')
    def test_predict_logistic_function(self, mock_vectorizer, mock_model):
        """Test de la fonction predict_logistic"""
        # Configuration des mocks
        mock_vectorizer.transform.return_value = Mock()
        mock_model.predict.return_value = np.array([1])
        mock_model.predict_proba.return_value = np.array([[0.3, 0.7]])

        # Test
        predicted_class, confidence, probabilities = predict_logistic("test text")

        # Vérifications
        assert predicted_class in [0, 1]
        assert 0 <= confidence <= 1
        assert "negative" in probabilities
        assert "positive" in probabilities


# Tests de validation des données
class TestDataValidation:
    """Tests de validation des données d'entrée"""

    def test_validate_whitespace_only(self):
        """Test avec seulement des espaces"""
        response = client.post("/predict", json={"text": "   "})

        assert response.status_code == 422

    def test_validate_special_characters(self):
        """Test avec des caractères spéciaux"""
        response = client.post("/predict", json={"text": "Test with emojis 😊🎉"})

        # Devrait fonctionner
        assert response.status_code in [200, 503]  # 503 si modèle non chargé

    def test_validate_numbers_only(self):
        """Test avec seulement des chiffres"""
        response = client.post("/predict", json={"text": "123456"})

        # Devrait fonctionner
        assert response.status_code in [200, 503]

    def test_validate_mixed_content(self):
        """Test avec du contenu mixte"""
        response = client.post("/predict", json={"text": "Test 123 #hashtag @mention"})

        # Devrait fonctionner
        assert response.status_code in [200, 503]


# Tests de performance
class TestPerformance:
    """Tests de performance (optionnels)"""

    @pytest.mark.slow
    @patch('app.model')
    @patch('app.tokenizer')
    def test_response_time(self, mock_tokenizer, mock_model, sample_tweet):
        """Test du temps de réponse"""
        import time

        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 102]]),
            'attention_mask': tf.constant([[1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.2, 0.8]])
        mock_model.return_value = mock_outputs

        # Mesure du temps
        start = time.time()
        response = client.post("/predict", json=sample_tweet)
        duration = time.time() - start

        # Le temps de réponse devrait être < 1 seconde
        assert response.status_code == 200
        assert duration < 1.0


# Tests d'intégration
class TestIntegration:
    """Tests d'intégration de bout en bout"""

    @patch('app.model')
    @patch('app.tokenizer')
    def test_full_workflow(self, mock_tokenizer, mock_model):
        """Test du workflow complet"""
        # Configuration des mocks
        mock_tokenizer.return_value = {
            'input_ids': tf.constant([[101, 2023, 102]]),
            'attention_mask': tf.constant([[1, 1, 1]])
        }

        mock_outputs = Mock()
        mock_outputs.logits = tf.constant([[0.2, 0.8]])
        mock_model.return_value = mock_outputs

        # 1. Vérifier que l'API est disponible
        response = client.get("/health")
        assert response.status_code == 200

        # 2. Faire une prédiction simple
        response = client.post("/predict", json={"text": "Great product!"})
        assert response.status_code == 200

        # 3. Faire une prédiction batch
        response = client.post("/predict/batch", json={
            "tweets": ["Great!", "Bad!", "Okay"]
        })
        assert response.status_code == 200
        assert response.json()["count"] == 3


# Configuration pytest
def pytest_configure(config):
    """Configuration de pytest"""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )


if __name__ == "__main__":
    # Exécuter les tests
    pytest.main([__file__, "-v", "--tb=short"])
