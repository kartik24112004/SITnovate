import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib

# Load Dataset
df = pd.read_csv("spam.csv", encoding="latin-1")

# Keep only necessary columns
df = df.iloc[:, [0, 1]]
df.columns = ['label', 'message']

# Convert labels to binary (ham = 0, spam = 1)
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Download stopwords if not already downloaded
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Text Preprocessing
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = " ".join(word for word in text.split() if word not in stop_words)
    return text

df['message'] = df['message'].apply(clean_text)

# Convert Text to Numeric Features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['message'])
y = df['label']

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# Save Model and Vectorizer
joblib.dump(model, "spam_model.pkl")
print("Model saved as spam_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")
print("Vectorizer saved as vectorizer.pkl")
