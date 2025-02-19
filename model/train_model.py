import pandas as pd
import nltk
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Download dataset (if using NLTK's stopwords)
nltk.download('stopwords')

# Load dataset (change path if necessary)
df = pd.read_csv("https://raw.githubusercontent.com/justmarkham/scikit-learn-videos/master/data/sms-spam.csv", encoding='latin-1')

# Rename columns
df.columns = ["label", "message"]
df = df[["message", "label"]]

# Convert labels to binary (spam = 1, ham = 0)
df["label"] = df["label"].map({"ham": 0, "spam": 1})

