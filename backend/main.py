from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles   # ADD THIS
from routers.interview_routes import router
from services.question_service import load_questions

app = FastAPI(
    title="AI Mock Interview Backend",
    version="1.0.0"
)

app.mount("/graphs", StaticFiles(directory="graphs"), name="graphs")


load_questions()

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AI Mock Interview Backend Running"}
