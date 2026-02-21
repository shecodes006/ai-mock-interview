import random


def generate_question(interview_type: str, difficulty: str):
    """
    Mock question generator (temporary until real GPT integration)
    """

    hr_questions = [
        "Tell me about yourself.",
        "What are your strengths and weaknesses?",
        "Why should we hire you?",
        "Describe a challenging situation you faced."
    ]

    technical_easy = [
        "What is Python?",
        "What is a variable?",
        "Explain OOPS concept.",
        "What is a function?"
    ]

    technical_medium = [
        "Explain REST API.",
        "What is multithreading?",
        "Difference between list and tuple?",
        "What is normalization in DB?"
    ]

    technical_hard = [
        "Explain microservices architecture.",
        "How does garbage collection work?",
        "Explain ACID properties.",
        "What is system design?"
    ]

    if interview_type.lower() == "hr":
        return random.choice(hr_questions)

    if difficulty.lower() == "easy":
        return random.choice(technical_easy)
    elif difficulty.lower() == "medium":
        return random.choice(technical_medium)
    else:
        return random.choice(technical_hard)


def evaluate_answer(answer: str):
    """
    Mock evaluation (simulates GPT scoring)
    """

    score = random.randint(5, 10)

    feedback_options = [
        "Good answer, but you can add more detail.",
        "Clear explanation, improve structure.",
        "Strong response with good clarity.",
        "Try to give more practical examples."
    ]

    feedback = random.choice(feedback_options)

    return {
        "score": score,
        "feedback": feedback
    }