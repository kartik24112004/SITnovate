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

# Ensure stopwords are downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

# Load Dataset (Fixed File Path Issue)
csv_path = r"C:\Users\Hp\Desktop\SITnovate\model\spam.csv"  # Using raw string to avoid Unicode error
if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Dataset not found at {csv_path}. Please check the path.")

df = pd.read_csv(csv_path, encoding="latin-1")

# Keep only necessary columns
df = df.iloc[:, [0, 1]]
df.columns = ["label", "message"]

# Convert labels to binary (ham = 0, spam = 1)
df["label"] = df["label"].map({"ham": 0, "spam": 1})

# Text Preprocessing Function
def clean_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)  # Remove punctuation
    text = " ".join(word for word in text.split() if word not in stop_words)  # Remove stopwords
    return text

df["message"] = df["message"].apply(clean_text)

# Convert Text to Numeric Features
vectorizer = TfidfVectorizer()
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
os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist

model_path = os.path.join(save_dir, "spam_model.pkl")
vectorizer_path = os.path.join(save_dir, "vectorizer.pkl")

joblib.dump(model, model_path)
print(f"Model saved as {model_path}")

joblib.dump(vectorizer, vectorizer_path)
print(f"Vectorizer saved as {vectorizer_path}")
