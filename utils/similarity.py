# utils/similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

# Einmaliger Vektorisierer für Effizienz
tfidf = TfidfVectorizer()

# Funktion zur Berechnung der Kosinus-Ähnlichkeit zwischen zwei Texten
def cosine_similarity(text1: str, text2: str) -> float:
    """
    Berechnet die Kosinus-Ähnlichkeit von zwei Texten basierend auf TF-IDF-Vektoren.
    Rückgabewert liegt zwischen 0.0 (völlig unterschiedlich) und 1.0 (identisch).
    """
    vectors = tfidf.fit_transform([text1, text2])
    score_matrix = cs(vectors[0:1], vectors[1:2])
    return float(score_matrix[0][0])
