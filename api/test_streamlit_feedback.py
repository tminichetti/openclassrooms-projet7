"""
Script de test pour vérifier que le système de feedback Streamlit fonctionne

Ce script simule l'envoi de feedback à Application Insights pour tester
la configuration sans avoir à utiliser l'interface Streamlit.

Usage:
    python test_streamlit_feedback.py
"""

import os
import logging
from datetime import datetime

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Configuration Azure Application Insights
APPINSIGHTS_INSTRUMENTATION_KEY = os.getenv("APPINSIGHTS_INSTRUMENTATION_KEY", "")
APPINSIGHTS_CONNECTION_STRING = os.getenv("APPINSIGHTS_CONNECTION_STRING", "")

# Flag pour activer/désactiver Application Insights
USE_APP_INSIGHTS = bool(APPINSIGHTS_CONNECTION_STRING or APPINSIGHTS_INSTRUMENTATION_KEY)

print("="*80)
print("TEST DU SYSTÈME DE FEEDBACK STREAMLIT")
print("="*80)
print()

# Vérifier la configuration
print("Configuration:")
print(f"  - APPINSIGHTS_CONNECTION_STRING: {'✅ Défini' if APPINSIGHTS_CONNECTION_STRING else '❌ Non défini'}")
print(f"  - APPINSIGHTS_INSTRUMENTATION_KEY: {'✅ Défini' if APPINSIGHTS_INSTRUMENTATION_KEY else '❌ Non défini'}")
print(f"  - Application Insights activé: {'✅ OUI' if USE_APP_INSIGHTS else '❌ NON'}")
print()

# Importer Application Insights si disponible
if USE_APP_INSIGHTS:
    try:
        from opencensus.ext.azure.log_exporter import AzureLogHandler

        if APPINSIGHTS_CONNECTION_STRING:
            logger.addHandler(AzureLogHandler(connection_string=APPINSIGHTS_CONNECTION_STRING))
        elif APPINSIGHTS_INSTRUMENTATION_KEY:
            logger.addHandler(AzureLogHandler(instrumentation_key=APPINSIGHTS_INSTRUMENTATION_KEY))

        print("✅ opencensus-ext-azure importé avec succès")
        print("✅ Azure Log Handler configuré")
        print()
    except ImportError:
        USE_APP_INSIGHTS = False
        print("❌ opencensus-ext-azure non installé")
        print("   Installez avec: pip install opencensus-ext-azure")
        print()
else:
    print("⚠️ Application Insights non configuré")
    print("   Définissez APPINSIGHTS_CONNECTION_STRING dans un fichier .env")
    print()


def send_test_feedback(text, predicted_sentiment, actual_sentiment, confidence, model_type="logistic"):
    """
    Envoie un feedback de test à Application Insights

    Args:
        text: Le texte du tweet
        predicted_sentiment: Sentiment prédit
        actual_sentiment: Sentiment réel
        confidence: Niveau de confiance
        model_type: Type de modèle
    """
    if USE_APP_INSIGHTS:
        try:
            logger.warning(
                f"[TEST] Prédiction incorrecte détectée",
                extra={
                    'custom_dimensions': {
                        'event_type': 'incorrect_prediction',
                        'test_mode': True,
                        'text': text[:100],
                        'text_length': len(text),
                        'predicted_sentiment': predicted_sentiment,
                        'actual_sentiment': actual_sentiment,
                        'confidence': confidence,
                        'model_type': model_type,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'test_script'
                    }
                }
            )
            print(f"✅ Trace envoyée: '{text[:50]}...'")
            return True
        except Exception as e:
            print(f"❌ Erreur lors de l'envoi: {e}")
            return False
    else:
        print(f"[LOCAL DEBUG] Feedback: '{text[:50]}...' - Prédit: {predicted_sentiment}, Réel: {actual_sentiment}")
        return False


# Tests
print("="*80)
print("ENVOI DE FEEDBACKS DE TEST")
print("="*80)
print()

test_cases = [
    {
        "text": "This flight was amazing! Best crew ever!",
        "predicted": "Négatif",
        "actual": "Positif",
        "confidence": 0.65
    },
    {
        "text": "Terrible experience. Flight delayed 5 hours.",
        "predicted": "Positif",
        "actual": "Négatif",
        "confidence": 0.72
    },
    {
        "text": "The service was okay, nothing special.",
        "predicted": "Positif",
        "actual": "Négatif",
        "confidence": 0.58
    }
]

success_count = 0
for i, test in enumerate(test_cases, 1):
    print(f"Test {i}/{len(test_cases)}:")
    print(f"  Texte: {test['text']}")
    print(f"  Prédit: {test['predicted']} (confiance: {test['confidence']:.0%})")
    print(f"  Réel: {test['actual']}")

    success = send_test_feedback(
        text=test['text'],
        predicted_sentiment=test['predicted'],
        actual_sentiment=test['actual'],
        confidence=test['confidence']
    )

    if success:
        success_count += 1

    print()

print("="*80)
print("RÉSUMÉ")
print("="*80)
print(f"Tests effectués: {len(test_cases)}")
print(f"Traces envoyées: {success_count}")
print(f"Mode: {'Application Insights' if USE_APP_INSIGHTS else 'Local (debug)'}")
print()

if USE_APP_INSIGHTS and success_count > 0:
    print("✅ SUCCÈS !")
    print()
    print("Pour vérifier dans Azure:")
    print("1. Aller dans le portail Azure → Application Insights")
    print("2. Menu 'Logs' ou 'Transaction search'")
    print("3. Exécuter cette requête:")
    print()
    print("   traces")
    print("   | where severityLevel >= 2")
    print("   | where customDimensions.test_mode == true")
    print("   | where customDimensions.source == 'test_script'")
    print("   | project timestamp, message, customDimensions")
    print("   | order by timestamp desc")
    print()
    print("Vous devriez voir vos 3 traces de test.")
elif not USE_APP_INSIGHTS:
    print("ℹ️ MODE LOCAL")
    print()
    print("Pour activer Application Insights:")
    print("1. Créer une ressource Application Insights dans Azure")
    print("2. Copier la Connection String")
    print("3. Créer un fichier .env avec:")
    print("   APPINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...")
    print("4. Relancer ce script")
else:
    print("❌ ÉCHEC")
    print("Vérifiez la configuration et réessayez.")

print()
print("="*80)
