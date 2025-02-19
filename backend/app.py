import os
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the directory of app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/spam_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../model/vectorizer.pkl")

print("Checking file paths...")
print("MODEL_PATH:", MODEL_PATH)
print("VECTORIZER_PATH:", VECTORIZER_PATH)

# Check if model files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"Vectorizer file not found at: {VECTORIZER_PATH}")

# Load the trained model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("Model and vectorizer loaded successfully!")

@app.route('/')
def home():
    return "Spam Email Classifier API is running!"

# API endpoint to predict spam or not spam
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get JSON input from frontend
    email_text = data.get('email', '').strip()  # Extract and clean email text

    if not email_text:
        return jsonify({"error": "No email text provided"}), 400

    # Transform text using the saved vectorizer
    email_vectorized = vectorizer.transform([email_text])

    # Predict using the model
    prediction = model.predict(email_vectorized)[0]

    return jsonify({"prediction": "Spam" if prediction == 1 else "Not Spam"})

if __name__ == '__main__':
    app.run(debug=True)
