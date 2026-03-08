import time
from services.gpt_services import evaluate_answer
from services.question_service import get_question
from services.resume_domain_service import detect_domain
from database.connection import get_connection
from services.analytics_service import generate_all_graphs


category_role_map = {
    "front-end": "Frontend Developer",
    "back-end": "Backend Developer",
    "full-stack": "Full Stack Developer",
    "data structures": "Software Engineer",
    "algorithms": "Software Engineer",
    "database and sql": "Database Developer",
    "database systems": "Database Engineer",
    "system design": "Backend Engineer",
    "distributed systems": "Distributed Systems Engineer",
    "machine learning": "Machine Learning Engineer",
    "artificial intelligence": "AI Engineer",
    "data engineering": "Data Engineer",
    "devops": "DevOps Engineer",
    "security": "Security Engineer",
    "networking": "Network Engineer",
    "software testing": "QA Engineer",
    "languages and frameworks": "Software Developer",
    "general programming": "Software Developer",
    "low-level systems": "Systems Engineer"
}

active_interviews = {}
uploaded_resumes = {}
uploaded_predictions = {}


def store_resume(user_id: str, resume_text: str):

    uploaded_resumes[user_id] = resume_text

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE id = %s",
        (user_id,)
    )

    user = cursor.fetchone()

    if not user:
        cursor.execute(
            """
            INSERT INTO users (id, user_identifier)
            VALUES (%s, %s)
            """,
            (user_id, f"user_{user_id}")
        )

    cursor.execute(
        """
        INSERT INTO resumes (user_id, resume_text)
        VALUES (%s, %s)
        """,
        (user_id, resume_text)
    )

    conn.commit()
    cursor.close()
    conn.close()


def store_predicted_roles(user_id: str, roles: list):
    uploaded_predictions[user_id] = roles


def start_interview(user_id: str, interview_type: str, difficulty: str, max_questions: int):

    if user_id in active_interviews:
        return {"error": "Interview already active for this user"}

    interview_type = interview_type.lower()
    difficulty = difficulty.lower()

    resume_text = uploaded_resumes.get(user_id)
    domain = None

    if interview_type == "technical" and resume_text:
        domain = detect_domain(resume_text)

    question_obj = get_question(
        interview_type,
        difficulty,
        [],
        domain=domain
    )

    if not question_obj:
        return {"error": "Unable to generate first question"}

    question_text = question_obj["question"]
    question_difficulty = question_obj.get("difficulty", difficulty).lower()

    if interview_type == "technical":
        question_category = question_obj.get("category")
    else:
        question_category = "behavioral"

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_sessions (user_id, interview_type, difficulty)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (user_id, interview_type, difficulty)
    )

    session_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    active_interviews[user_id] = {
        "session_id": session_id,
        "question_count": 0,
        "max_questions": max_questions,
        "start_time": time.time(),
        "type": interview_type,
        "difficulty": difficulty,
        "domain": domain,
        "questions": [question_text],
        "categories": [question_category],
        "difficulties": [question_difficulty],
        "answers": [],
        "scores": [],
        "feedbacks": []
    }

    return {
        "status": "started",
        "type": interview_type,
        "difficulty": difficulty,
        "domain_detected": domain,
        "max_questions": max_questions,
        "time_limit_seconds": 300,
        "question": question_text
    }


def submit_answer(user_id: str, answer: str):

    if user_id not in active_interviews:
        return {"error": "Interview not found"}

    session = active_interviews[user_id]

    elapsed_time = time.time() - session["start_time"]
    remaining_time = 300 - elapsed_time

    if remaining_time <= 0:
        return finalize_interview(user_id, reason="Time limit exceeded")

    current_question = session["questions"][-1]
    current_category = session["categories"][-1]
    current_difficulty = session["difficulties"][-1].lower()

    evaluation = evaluate_answer(answer)
    score = evaluation["score"]
    feedback = evaluation["feedback"]

    conn = get_connection()
    cursor = conn.cursor()

    session_id = session["session_id"]

    cursor.execute(
        """
        INSERT INTO interview_questions
        (session_id, question, answer, score, feedback, category, difficulty)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
        (
            session_id,
            current_question,
            answer,
            score,
            feedback,
            current_category,
            current_difficulty
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    session["answers"].append(answer)
    session["scores"].append(score)
    session["feedbacks"].append(feedback)

    session["question_count"] += 1
    remaining_questions = session["max_questions"] - session["question_count"]

    if remaining_questions <= 0:
        return finalize_interview(user_id, reason="Max questions reached")

    next_question_obj = get_question(
        session["type"],
        session["difficulty"],
        session["questions"],
        domain=session.get("domain")
    )

    if not next_question_obj:
        return finalize_interview(user_id, reason="No more questions available")

    next_text = next_question_obj["question"]
    next_difficulty = next_question_obj.get("difficulty", session["difficulty"]).lower()

    if session["type"] == "technical":
        next_category = next_question_obj.get("category")
    else:
        next_category = "behavioral"

    session["questions"].append(next_text)
    session["categories"].append(next_category)
    session["difficulties"].append(next_difficulty)

    return {
        "status": "continue",
        "current_question_number": session["question_count"],
        "remaining_questions": remaining_questions,
        "remaining_time_seconds": int(remaining_time),
        "score": score,
        "feedback": feedback,
        "next_question": next_text
    }


def finalize_interview(user_id: str, reason: str):

    session = active_interviews.get(user_id)

    if not session:
        return {"error": "Interview session not found or already ended"}

    total_questions = len(session["scores"])
    total_score = sum(session["scores"])
    average_score = round(total_score / total_questions, 2) if total_questions > 0 else 0

    max_possible_score = total_questions * 10
    final_percentage = round((total_score / max_possible_score) * 100, 2) if max_possible_score > 0 else 0

    if average_score >= 8:
        performance = "Excellent"
    elif average_score >= 6:
        performance = "Good"
    elif average_score >= 4:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    category_scores = {}

    for i in range(len(session["scores"])):
        category = session["categories"][i]
        score = session["scores"][i]
        category_scores.setdefault(category, []).append(score)

    category_averages = {
        cat: round(sum(scores) / len(scores), 2)
        for cat, scores in category_scores.items()
    }

    strongest_category = max(category_averages, key=category_averages.get) if category_averages else None

    score_progression = [
        {"question": i + 1, "score": session["scores"][i]}
        for i in range(len(session["scores"]))
    ]

    weak_categories = [
        cat for cat, avg in category_averages.items()
        if avg < 6
    ]

    improvement_suggestions = [
        f"Practice more problems on {cat}"
        for cat in weak_categories
    ]

    resume_domain = session.get("domain")
    resume_roles = uploaded_predictions.get(user_id, [])

    strongest_role = category_role_map.get(strongest_category, "Software Engineer")

    final_roles = []
    final_roles.append(strongest_role)

    for role in resume_roles:
        if role not in final_roles:
            final_roles.append(role)

    final_roles = final_roles[:5]

    if resume_domain and resume_domain == strongest_category:
        confidence = "High (Resume + Interview aligned)"
    elif resume_domain and resume_domain != strongest_category:
        confidence = "Medium (Interview stronger than resume)"
    else:
        confidence = "Based on interview performance only"

    # ----------------------------
    # GENERATE ANALYTICS GRAPHS
    # ----------------------------

    graphs = generate_all_graphs(
        session["session_id"],
        session["scores"],
        category_averages
    )

    result = {
        "status": "ended",
        "reason": reason,
        "total_questions": total_questions,
        "average_score": average_score,
        "final_percentage": final_percentage,
        "performance": performance,
        "strongest_category": strongest_category,
        "weak_categories": weak_categories,
        "improvement_suggestions": improvement_suggestions,
        "category_breakdown": category_averages,
        "resume_detected_domain": resume_domain,
        "suggested_roles": final_roles,
        "confidence_level": confidence,
        "score_progression": score_progression,
        "graphs": graphs,
        "all_scores": session["scores"],
        "all_questions": session["questions"],
        "all_answers": session["answers"],
        "all_feedbacks": session["feedbacks"]
    }

    # -------------------------------
    # UPDATE INTERVIEW SESSION IN DB
    # -------------------------------

    conn = get_connection()
    cursor = conn.cursor()

    session_id = session["session_id"]

    cursor.execute(
        """
        UPDATE interview_sessions
        SET total_questions = %s,
            average_score = %s,
            final_percentage = %s,
            performance = %s,
            detected_domain = %s,
            strongest_category = %s,
            suggested_role = %s,
            suggested_roles = %s,
            total_time_seconds = %s
        WHERE id = %s
        """,
        (
            total_questions,
            average_score,
            final_percentage,
            performance,
            resume_domain,
            strongest_category,
            final_roles[0] if final_roles else None,
            final_roles,
            int(time.time() - session["start_time"]),
            session_id
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    del active_interviews[user_id]

    return result

def get_interview_result(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            total_questions,
            average_score,
            final_percentage,
            performance,
            detected_domain,
            strongest_category,
            suggested_roles
        FROM interview_sessions
        WHERE user_id = %s
        ORDER BY id DESC
        LIMIT 1
        """,
        (user_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return {"error": "No interview result found"}

    session_id = row[0]

    graphs = {
        "score_progression": f"graphs/session_{session_id}_score_progression.png",
        "category_performance": f"graphs/session_{session_id}_category_performance.png",
        "skill_strength": f"graphs/session_{session_id}_skill_strength.png",
        "score_pie": f"graphs/session_{session_id}_score_pie.png",
        "score_histogram": f"graphs/session_{session_id}_score_histogram.png"
    }

    return {
        "session_id": session_id,
        "total_questions": row[1],
        "average_score": row[2],
        "final_percentage": row[3],
        "performance": row[4],
        "detected_domain": row[5],
        "strongest_category": row[6],
        "suggested_roles": row[7],
        "graphs": graphs
    }

def end_interview(user_id: str):
    if user_id not in active_interviews:
        return {"error": "No active interview found"}

    return finalize_interview(user_id, reason="Interview manually ended")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def generate_progress_graph(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, final_percentage
        FROM interview_sessions
        WHERE user_id = %s
        ORDER BY id
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return None

    session_ids = [row[0] for row in rows]
    scores = [row[1] for row in rows]

    plt.figure(figsize=(8,5))

    plt.plot(session_ids, scores, marker="o")

    plt.title("Interview Progress Over Time")
    plt.xlabel("Interview Session")
    plt.ylabel("Score (%)")
    plt.grid(True)

    path = f"graphs/user_{user_id}_progress.png"

    plt.tight_layout()
    plt.savefig(path)
    plt.close()

    return path


def get_interview_history(user_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            total_questions,
            average_score,
            final_percentage,
            performance,
            strongest_category,
            suggested_roles
        FROM interview_sessions
        WHERE user_id = %s
        ORDER BY id DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "session_id": row[0],
            "total_questions": row[1],
            "average_score": row[2],
            "final_percentage": row[3],
            "performance": row[4],
            "strongest_category": row[5],
            "suggested_roles": row[6]
        })

    progress_graph = generate_progress_graph(user_id)

    return {
        "user_id": user_id,
        "total_interviews": len(history),
        "history": history,
        "progress_graph": progress_graph
    }