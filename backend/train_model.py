import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
df = pd.read_csv("backend/data/resume_cleaned.csv")

allowed_roles = [
"Senior Software Engineer",
"Machine Learning (ML) Engineer",
"AI Engineer",
"Senior iOS Engineer",
"DevOps Engineer",
"Data Engineer",
"Full Stack Developer (Python,React js)",
"Data Science Engineer",
"Database Administrator (DBA)",
"Network Support Engineer",
"System Administrator (Operation & Maintenance of Server, Storage & Service Desk System)",
"Executive/ Sr. Executive -IT",
"Intern (Generative AI Engineering - 2D/3D Image Generation)"
]

df = df[df["job_position_name"].isin(allowed_roles)]

# Features and labels
X = df["resume_text"]
y = df["job_position_name"]

# Convert text to TF-IDF
vectorizer = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_tfidf = vectorizer.fit_transform(X)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_tfidf, y,
    test_size=0.2,
    random_state=42
)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:", accuracy)

# Save model
with open("backend/models/job_role_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save vectorizer
with open("backend/models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")