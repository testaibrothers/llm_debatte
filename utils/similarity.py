# utils/similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

# Einmaliger Vektorisierer für Effizienz
tfidf = TfidfVectorizer()

def cosine_similarity(text1: str, text2: str) -> float:
    """
    Berechnet die Kosinus-Ähnlichkeit zwischen zwei Texten basierend auf TF-IDF-Vektoren.
    Rückgabewert zwischen 0.0 und 1.0.
    """
    vectors = tfidf.fit_transform([text1, text2])
    similarity_matrix = cs(vectors[0:1], vectors[1:2])
    return float(similarity_matrix[0][0])
