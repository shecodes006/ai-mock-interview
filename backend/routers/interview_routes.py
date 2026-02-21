from fastapi import APIRouter
from services.interview_logic import start_interview, submit_answer, end_interview

router = APIRouter()

@router.post("/interview/start")
def start(user_id: str, interview_type: str, difficulty: str, max_questions: int):
    return start_interview(user_id, interview_type, difficulty, max_questions)

@router.post("/interview/answer")
def answer(user_id: str, answer: str):
    return submit_answer(user_id, answer)


@router.get("/interview/result")
def get_result():
    return {"message": "Result logic coming in Phase 6"}

@router.post("/interview/end")
def end(user_id: str):
    return end_interview(user_id)