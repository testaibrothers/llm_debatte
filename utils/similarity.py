from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs

# Initialize vectorizer once for efficiency
vectorizer = TfidfVectorizer()

def cosine_similarity(text1: str, text2: str) -> float:
    tfidf = vectorizer.fit_transform([text1, text2])
    mat = cs(tfidf[0:1], tfidf[1:2])
    return float(mat[0][0])
