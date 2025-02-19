import joblib

print("Loading vectorizer and model...")
vectorizer = joblib.load("vectorizer_test.pkl")
model = joblib.load("spam_model.pkl")
print("Vectorizer and model loaded successfully.")

sample_text = ["You won a lottery! Claim your prize now."]
print("Sample text:", sample_text)

X_test = vectorizer.transform(sample_text)
print("Transformed text shape:", X_test.shape)

prediction = model.predict(X_test)
print("Raw prediction output:", prediction)

print("Prediction:", "Spam" if prediction[0] == 1 else "Not Spam")
