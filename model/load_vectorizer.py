import joblib

# Load the saved vectorizer
vectorizer = joblib.load("vectorizer_test.pkl")
print("Vectorizer loaded successfully!")
