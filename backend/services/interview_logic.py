import time
#this will store active interview sessions temporarily till phase 4
from services.gpt_services import generate_question, evaluate_answer

active_interviews ={}

def start_interview(user_id: str, interview_type: str, difficulty: str, max_questions: int):

    # Prevent duplicate session
    if user_id in active_interviews:
        return {"error": "Interview already active for this user"}

    active_interviews[user_id] = {
        "question_count": 0,
        "max_questions": max_questions,
        "start_time": time.time(),
        "type": interview_type,
        "difficulty": difficulty
    }

    first_question = generate_question(interview_type, difficulty)
    return {
        "status": "started",
        "type": interview_type,
        "difficulty": difficulty,
        "max_questions": max_questions,
        "time_limit_seconds": 300,
        "question": first_question
    }


def submit_answer(user_id: str, answer: str):

    if user_id not in active_interviews:
        return {"error": "Interview not found"}

    session = active_interviews[user_id]

    elapsed_time = time.time() - session["start_time"]
    remaining_time = 300 - elapsed_time

    if remaining_time <= 0:
        del active_interviews[user_id]
        return {
            "status": "ended",
            "reason": "Time limit exceeded"
        }

    # Evaluate answer
    evaluation = evaluate_answer(answer)
    score = evaluation["score"]
    feedback = evaluation["feedback"]

    session["question_count"] += 1
    remaining_questions = session["max_questions"] - session["question_count"]

    if remaining_questions <= 0:
        del active_interviews[user_id]
        return {
            "status": "ended",
            "reason": "Max questions reached",
            "score": score,
            "feedback": feedback
        }

    next_question = generate_question(session["type"], session["difficulty"])

    return {
        "status": "continue",
        "current_question_number": session["question_count"],
        "remaining_questions": remaining_questions,
        "remaining_time_seconds": int(remaining_time),
        "score": score,
        "feedback": feedback,
        "next_question": next_question
    }

def end_interview(user_id: str):

    if user_id not in active_interviews:
        return {"error": "No active interview found"}

    del active_interviews[user_id]

    return {
        "status": "ended",
        "reason": "Interview manually ended"
    }