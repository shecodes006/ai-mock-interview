import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model_path = os.path.join(BASE_DIR, "models", "job_role_model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "models", "vectorizer.pkl")

with open(model_path, "rb") as f:
    model = pickle.load(f)

with open(vectorizer_path, "rb") as f:
    vectorizer = pickle.load(f)


# Define allowed TECH roles
TECH_KEYWORDS = [
    "engineer",
    "developer",
    "data",
    "ai",
    "machine learning",
    "devops",
    "administrator",
    "network",
    "software",
    "full stack",
    "backend",
    "frontend"
]


def is_tech_role(role_name):
    role_name = role_name.lower()
    return any(keyword in role_name for keyword in TECH_KEYWORDS)


def predict_job_role(resume_text: str):

    # Convert resume text into TF-IDF vector
    resume_vector = vectorizer.transform([resume_text])

    # Get probability for every role
    probabilities = model.predict_proba(resume_vector)[0]

    roles = model.classes_

    role_prob_pairs = list(zip(roles, probabilities))

    # Filter only TECH roles
    tech_roles = [(role, prob) for role, prob in role_prob_pairs if is_tech_role(role)]

    # If filtering removed everything, fallback to all roles
    if len(tech_roles) == 0:
        tech_roles = role_prob_pairs

    # Sort roles by probability
    tech_roles = sorted(tech_roles, key=lambda x: x[1], reverse=True)

    # Take top 5 roles
    top_roles = [role for role, _ in tech_roles[:5]]

    confidence = tech_roles[0][1]

    return top_roles, round(float(confidence), 2)

