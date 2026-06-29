import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_excel("telangana_public_pulse.xlsx")

# Prepare data
df = df[['text', 'sentiment']].dropna()
df['text'] = df['text'].astype(str).str.lower()

X = df['text']
y = df['sentiment']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Vectorize
vectorizer = TfidfVectorizer(ngram_range=(1,2), max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

# Save locally (VERY IMPORTANT)
joblib.dump(model, "sentiment_model (1).pkl")
joblib.dump(vectorizer, "vectorizer (2).pkl")

print("✅ Model saved successfully!")