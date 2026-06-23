from fastapi import FastAPI
from app.routes import tasks, auth

app = FastAPI(title="Task Manager — DevOps Demo")

app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/health")
def health():
    return {"status": "ok"}
