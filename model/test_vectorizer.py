import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Create a test vectorizer
vectorizer = TfidfVectorizer()
joblib.dump(vectorizer, "vectorizer_test.pkl")

print("Vectorizer manually saved as vectorizer_test.pkl!")
