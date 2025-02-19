import joblib

# Load the trained model and vectorizer
try:
    model = joblib.load("spam_model.pkl")  # Load the trained model
    vectorizer = joblib.load("vectorizer.pkl")  # Load the TF-IDF vectorizer
except FileNotFoundError as e:
    print(f"Error: {e}")
    print("Make sure 'spam_model.pkl' and 'vectorizer.pkl' exist in the directory.")
    exit()

# Function to make predictions
def predict_spam(text):
    transformed_text = vectorizer.transform([text])  # Convert text to TF-IDF features
    prediction = model.predict(transformed_text)  # Make prediction
    return "Spam" if prediction[0] == 1 else "Ham"

# Example Test Cases
test_messages = [
    "Congratulations! You've won a free vacation. Click here to claim now!",
    "Hey, can we meet tomorrow for the project discussion?",
    "Exclusive offer just for you! Get a discount now.",
]

# Run predictions
for msg in test_messages:
    print(f"Message: {msg}")
    print(f"Prediction: {predict_spam(msg)}\n")
