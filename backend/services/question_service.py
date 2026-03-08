import pandas as pd
import random
import os

technical_questions = []
hr_questions = []


def load_questions():
    global technical_questions, hr_questions

    base_path = os.path.dirname(os.path.dirname(__file__))
    data_path = os.path.join(base_path, "data")

    technical_path = os.path.join(data_path, "interview_questions.csv")
    hr_path = os.path.join(data_path, "hr_questions.csv")

    tech_df = pd.read_csv(technical_path)
    hr_df = pd.read_csv(hr_path)

    technical_questions = tech_df.to_dict(orient="records")
    hr_questions = hr_df.to_dict(orient="records")

    print(f"Loaded {len(technical_questions)} technical questions")
    print(f"Loaded {len(hr_questions)} HR questions")


def get_question(interview_type, difficulty, asked_questions, domain=None):
    difficulty = difficulty.lower()

    if interview_type == "technical":
        pool = technical_questions
    else:
        pool = hr_questions

    # Filter by difficulty & not already asked
    filtered = [
        q for q in pool
        if q["difficulty"].lower() == difficulty
        and q["question"] not in asked_questions
    ]

    # Try domain filtering (technical only)
    if interview_type == "technical" and domain:
        domain_filtered = [
            q for q in filtered
            if q["category"].lower() == domain.lower()
        ]

        if domain_filtered:
            return random.choice(domain_filtered)

    # Fallback: any filtered
    if filtered:
        return random.choice(filtered)

    # Final fallback: ignore difficulty
    fallback = [
        q for q in pool
        if q["question"] not in asked_questions
    ]

    if fallback:
        return random.choice(fallback)

    return None