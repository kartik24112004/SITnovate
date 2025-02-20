import pandas as pd
import re
import string
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import numpy as np
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()

def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)  # Remove punctuation
    words = text.split()
    words = [stemmer.stem(word) for word in words if word not in stop_words]  # Apply stemming
    return " ".join(words)

# Ensure stopwords are downloaded
nltk.download("stopwords", quiet=True)
stop_words = set(stopwords.words("english"))

# Load Dataset (Fix file path issue)
csv_path = r"C:\Users\Hp\Desktop\SITnovate\model\spam.csv"  # Use raw string (r"...")
df = pd.read_csv(csv_path, encoding="latin-1")

# Keep only necessary columns (Check if correct columns exist)
df = df.iloc[:, [0, 1]]
df.columns = ["label", "message"]

# Convert labels to binary (ham = 0, spam = 1)
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Check label distribution (Now df is defined)
unique, counts = np.unique(df["label"], return_counts=True)
print(dict(zip(unique, counts)))  # Check spam (1) vs. ham (0) ratio

# Text Preprocessing Function
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    text = " ".join(word for word in text.split() if word not in stop_words)
    return text

df["message"] = df["message"].apply(clean_text)

# Convert Text to Numeric Features
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X = vectorizer.fit_transform(df["message"])
y = df["label"]

# Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = MultinomialNB()
model.fit(X_train, y_train)

# Evaluate Model
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
print(f"Precision: {precision_score(y_test, y_pred):.2f}")
print(f"Recall: {recall_score(y_test, y_pred):.2f}")
print(f"F1 Score: {f1_score(y_test, y_pred):.2f}")

# Save Model and Vectorizer
save_dir = r"C:\Users\Hp\Desktop\SITnovate\model"
os.makedirs(save_dir, exist_ok=True)  # Create directory if not exists

joblib.dump(model, os.path.join(save_dir, "spam_model.pkl"))
print(f"Model saved as {os.path.join(save_dir, 'spam_model.pkl')}")

joblib.dump(vectorizer, os.path.join(save_dir, "vectorizer.pkl"))
print(f"Vectorizer saved as {os.path.join(save_dir, 'vectorizer.pkl')}")