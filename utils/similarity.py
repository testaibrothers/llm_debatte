# utils/similarity.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

# Einmaliger Vektorisierer für Effizienz
tfidf = TfidfVectorizer()

def cosine_similarity(text1: str, text2: str) -> float:
    vecs = tfidf.fit_transform([text1, text2])
    score = cs(vecs[0:1], vecs[1:2])[0][0]
    return float(score)
