import os
import joblib
import json

import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

firebase_cred_json = os.getenv("FIREBASE_CRED_JSON")

if firebase_cred_json:
    cred = credentials.Certificate(json.loads(firebase_cred_json))
    firebase_admin.initialize_app(cred)
else:
    raise ValueError("Firebase credentials not found in environment variables")
# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow frontend communication

# Get the base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths for model and vectorizer
MODEL_PATH = os.path.join(BASE_DIR, "../model/spam_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../model/vectorizer.pkl")
FIREBASE_CREDENTIALS = os.path.join(BASE_DIR, "../firebase/serviceAccountKey.json")

from flask import Flask, request, jsonify

app = Flask(__name__)

# Get the directory of app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../model/spam_model.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "../model/vectorizer.pkl")

print("Checking file paths...")
print("MODEL_PATH:", MODEL_PATH)
print("VECTORIZER_PATH:", VECTORIZER_PATH)

print("FIREBASE_CREDENTIALS:", FIREBASE_CREDENTIALS)

# Ensure all required files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"Vectorizer file not found: {VECTORIZER_PATH}")
if not os.path.exists(FIREBASE_CREDENTIALS):
    raise FileNotFoundError(f"Firebase credentials file not found: {FIREBASE_CREDENTIALS}")


# Check if model files exist
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")

if not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError(f"Vectorizer file not found at: {VECTORIZER_PATH}")


# Load the trained model and vectorizer
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("Model and vectorizer loaded successfully!")

# Initialize Firebase (prevent multiple initializations)
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS)
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()


###  FUNCTION TO CLASSIFY EMAIL TEXT ###
def classify_email(email_text):
    if not email_text.strip():
        return "Invalid Input: Empty Email"

    email_vectorized = vectorizer.transform([email_text])
    prediction = model.predict(email_vectorized)[0]
    spam_probability = model.predict_proba(email_vectorized)[:, 1][0]  # Get spam probability

    return {"prediction": "Spam" if prediction == 1 else "Not Spam", "spam_probability": round(spam_probability, 2)}


###  STORE CLASSIFICATION RESULT IN FIREBASE ###
def store_email(email_text, prediction, spam_probability):
    db.collection("emails").add({
        "email_text": email_text,
        "prediction": prediction,
        "spam_probability": spam_probability
    })
    print("Email stored in Firestore!")


###  API ROUTES ###

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Spam Email Classifier API is running!"})


# API Endpoint to Predict Spam or Not Spam
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        email_text = data.get('email', '').strip()

        if not email_text:
            return jsonify({"error": "No email text provided"}), 400

        # Classify the email
        result = classify_email(email_text)

        # Store result in Firebase
        store_email(email_text, result["prediction"], result["spam_probability"])

        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API Endpoint to Retrieve All Stored Emails
@app.route('/get_emails', methods=['GET'])
def get_emails():
    try:
        emails_ref = db.collection("emails").stream()
        emails_list = [{"email_text": doc.to_dict().get("email_text"),
                        "prediction": doc.to_dict().get("prediction"),
                        "spam_probability": doc.to_dict().get("spam_probability", "N/A")}
                       for doc in emails_ref]

        return jsonify({"emails": emails_list})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


###  START FLASK SERVER ###
if __name__ == '__main__':
    print("Starting Flask server at http://127.0.0.1:5000/")
    app.run(debug=True)


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
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


