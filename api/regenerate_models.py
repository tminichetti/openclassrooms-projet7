"""
Script pour régénérer les modèles légers avec les bonnes dépendances

Ce script recharge les modèles depuis le dossier parent et les sauvegarde correctement
pour s'assurer qu'ils sont compatibles avec scikit-learn 1.3.2
"""

import joblib
import os
import sys

print("Régénération des modèles pour l'API...")

# Charger depuis le dossier parent
parent_models_dir = "../models"
api_models_dir = "./models"

# Créer le dossier models dans api si nécessaire
os.makedirs(api_models_dir, exist_ok=True)

# Charger le modèle de régression logistique
model_path = os.path.join(parent_models_dir, "logistic_regression_model.pkl")
vectorizer_path = os.path.join(parent_models_dir, "tfidf_vectorizer.pkl")

print(f"\nChargement du modèle depuis: {model_path}")
print(f"Existe: {os.path.exists(model_path)}")

if not os.path.exists(model_path):
    print("❌ Fichier modèle non trouvé!")
    sys.exit(1)

if not os.path.exists(vectorizer_path):
    print("❌ Fichier vectorizer non trouvé!")
    sys.exit(1)

# Charger
print("\nChargement des fichiers...")
model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)

print(f"✓ Modèle chargé: {type(model)}")
print(f"✓ Vectorizer chargé: {type(vectorizer)}")

# Vérifier le vectorizer
print(f"\nVérification du vectorizer:")
print(f"  - Has idf_: {hasattr(vectorizer, 'idf_')}")
print(f"  - Has vocabulary_: {hasattr(vectorizer, 'vocabulary_')}")

if hasattr(vectorizer, 'vocabulary_'):
    print(f"  - Vocabulary size: {len(vectorizer.vocabulary_)}")

if not hasattr(vectorizer, 'idf_'):
    print("\n⚠️  WARNING: Le vectorizer n'a pas d'attribut idf_!")
    print("   Il n'est probablement pas fitté correctement.")
    print("   Vous devez le réentraîner depuis le notebook.")
    sys.exit(1)

# Sauvegarder dans le dossier api/models
new_model_path = os.path.join(api_models_dir, "logistic_regression_model.pkl")
new_vectorizer_path = os.path.join(api_models_dir, "tfidf_vectorizer.pkl")

print(f"\nSauvegarde vers:")
print(f"  - {new_model_path}")
print(f"  - {new_vectorizer_path}")

joblib.dump(model, new_model_path)
joblib.dump(vectorizer, new_vectorizer_path)

print("\n✅ Modèles régénérés avec succès!")

# Test rapide
print("\nTest de transformation...")
test_text = ["This is a test"]
try:
    result = vectorizer.transform(test_text)
    print(f"✓ Transform fonctionne! Shape: {result.shape}")
except Exception as e:
    print(f"❌ Erreur lors du transform: {e}")
    sys.exit(1)

print("\n🎉 Tout est prêt pour le déploiement!")
