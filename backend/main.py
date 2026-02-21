from fastapi import FastAPI
from routers.interview_routes import router

app = FastAPI(
    title="AI Mock Interview Backend",
   
)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "AI Mock Interview Backend Running"}
