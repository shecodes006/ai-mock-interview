from fastapi import APIRouter, UploadFile, File
from services.resume_service import extract_text_from_pdf
from services.interview_logic import start_interview, submit_answer, end_interview, store_resume, store_predicted_roles, finalize_interview
from services.predict_role import predict_job_role
from services.interview_logic import get_interview_result
from services.interview_logic import get_interview_history   # PHASE 6
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

@router.post("/interview/start")
def start(user_id: str, interview_type: str, difficulty: str, max_questions: int):
    return start_interview(user_id, interview_type, difficulty, max_questions)


@router.post("/interview/answer")
def answer(user_id: str, answer: str):
    return submit_answer(user_id, answer)


# RESULT ENDPOINT (returns analytics + graphs)
@router.get("/interview/result")
def get_result(user_id: str):
    return get_interview_result(user_id)


# PHASE 6 → Interview History + Progress Graph
@router.get("/interview/history")
def interview_history(user_id: str):
    return get_interview_history(user_id)


@router.get("/interview/graphs", response_class=HTMLResponse)
def show_graphs(user_id: str):

    from database.connection import get_connection
    import os

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    SELECT id
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
        return {"error": "No interview found"}

    session_id = row[0]

    graph_dir = "graphs"

    session_graphs = [
        f for f in os.listdir(graph_dir)
        if f.startswith(f"session_{session_id}_")
     ]

    progress_graph = f"user_{user_id}_progress.png"

    graphs = session_graphs.copy()

    if progress_graph in os.listdir(graph_dir):
        graphs.append(progress_graph)

    if not graphs:
        return {"error": "Graphs not generated yet"}

    html_images = ""

    for graph in graphs:
        html_images += f'''
        <div class="graph">
        <img src="/graphs/{graph}">
        </div>
        '''

    html = f"""
<html>
<head>
<title>Interview Analytics</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background-color: #f4f6f9;
    margin: 0;
    padding: 20px;
    text-align: center;
}}

h1 {{
    margin-bottom: 40px;
}}

.container {{
    width: 80%;
    margin: auto;
}}

.graph {{
    background: white;
    padding: 20px;
    margin-bottom: 35px;
    border-radius: 10px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.1);
}}

.graph img {{
    width: 100%;
    height: auto;
}}

</style>

</head>

<body>

<h1>Interview Analytics Dashboard</h1>

<div class="container">
{html_images}
</div>

</body>
</html>
"""
    return html


@router.post("/interview/end")
def end(user_id: str):
    return end_interview(user_id)


@router.post("/resume/upload")
async def upload_resume(user_id: str, file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are allowed"}

    # Extract resume text
    extracted_text = extract_text_from_pdf(file)

    # ML prediction (TOP 5 roles)
    predicted_roles, confidence = predict_job_role(extracted_text)

    print("Top predicted roles:", predicted_roles)
    print("Confidence:", confidence)

    # Store resume text
    store_resume(user_id, extracted_text)

    # Store predicted roles for later use in final interview result
    store_predicted_roles(user_id, predicted_roles)

    return {
        "status": "success",
        "filename": file.filename,
        "predicted_roles": predicted_roles,
        "confidence": confidence,
        "preview": extracted_text[:300]
    }