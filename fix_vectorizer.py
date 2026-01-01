"""
Script pour corriger le vectorizer TF-IDF

Ce script recharge les données d'entraînement, refit le vectorizer et le sauvegarde correctement
"""

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import os

print("🔧 Correction du vectorizer TF-IDF...")

# Charger les données
print("\n1. Chargement des données...")
try:
    # Charger train_lemmatized (données preprocessées)
    data_path = "data/processed/train_lemmatized.csv"

    if not os.path.exists(data_path):
        print(f"❌ Fichier non trouvé: {data_path}")
        import sys
        sys.exit(1)

    df = pd.read_csv(data_path)
    print(f"✓ Données chargées: {len(df)} tweets")

except Exception as e:
    print(f"❌ Erreur lors du chargement des données: {e}")
    print("\nSi vous avez les données preprocessées, modifiez data_path dans ce script.")
    import sys
    sys.exit(1)

# Identifier la colonne de texte
text_column = 'text'  # Colonne dans les données preprocessées

if text_column not in df.columns:
    print(f"❌ Colonne '{text_column}' non trouvée. Colonnes disponibles: {list(df.columns)}")
    import sys
    sys.exit(1)

print(f"✓ Utilisation de la colonne: {text_column}")
print(f"✓ Colonnes disponibles: {list(df.columns)}")

# Créer le vectorizer
print("\n2. Création et fit du vectorizer...")
tfidf = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 2),
    min_df=5,
    max_df=0.8
)

# Fit sur toutes les données (train + test)
X_tfidf = tfidf.fit_transform(df[text_column].fillna(''))

print(f"✓ Vectorizer fitté")
print(f"  - Vocabulary size: {len(tfidf.vocabulary_)}")
print(f"  - Matrix shape: {X_tfidf.shape}")
print(f"  - Has idf_: {hasattr(tfidf, 'idf_')}")

# Sauvegarder
print("\n3. Sauvegarde...")
output_path = "models/tfidf_vectorizer.pkl"
os.makedirs("models", exist_ok=True)

joblib.dump(tfidf, output_path)
print(f"✓ Vectorizer sauvegardé: {output_path}")

# Vérifier en rechargeant
print("\n4. Vérification...")
tfidf_loaded = joblib.load(output_path)
print(f"✓ Vectorizer rechargé")
print(f"  - Has idf_: {hasattr(tfidf_loaded, 'idf_')}")
print(f"  - Vocabulary size: {len(tfidf_loaded.vocabulary_)}")

# Test de transformation
test_text = ["This flight was amazing!"]
result = tfidf_loaded.transform(test_text)
print(f"✓ Test de transformation réussi: {result.shape}")

# Copier vers api/models
print("\n5. Copie vers api/models...")
api_output_path = "api/models/tfidf_vectorizer.pkl"
os.makedirs("api/models", exist_ok=True)
joblib.dump(tfidf, api_output_path)
print(f"✓ Copié vers: {api_output_path}")

print("\n✅ Vectorizer corrigé avec succès!")
print(f"\nFichiers créés:")
print(f"  - {output_path}")
print(f"  - {api_output_path}")
print("\nVous pouvez maintenant commit et push ces fichiers sur GitHub.")
