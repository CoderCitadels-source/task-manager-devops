from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate, TaskStatus
from app.routes.auth import get_current_user
from datetime import date

router = APIRouter(prefix="/tasks", tags=["tasks"])

# In-memory store for demo purposes
_tasks = {}
_next_id = 1


@router.get("/", response_model=List[TaskOut])
def list_tasks(current_user: dict = Depends(get_current_user)):
    # return tasks owned by current user
    return [t for t in _tasks.values() if t.get("owner") == current_user["username"]]


@router.post("/", response_model=TaskOut)
def create_task(payload: TaskCreate, current_user: dict = Depends(get_current_user)):
    global _next_id
    task = {
        "id": _next_id,
        "title": payload.title,
        "description": payload.description,
        "due_date": payload.due_date,
        "status": TaskStatus.todo,
        "owner": current_user["username"],
    }
    _tasks[_next_id] = task
    _next_id += 1
    return task


@router.get("/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    # simple dashboard counts
    tasks = [t for t in _tasks.values() if t.get("owner") == current_user["username"]]
    total = len(tasks)
    by_status = {s.value: 0 for s in TaskStatus}
    upcoming = None
    for t in tasks:
        by_status[t["status"].value if hasattr(t["status"], "value") else t["status"]] += 1
        if t.get("due_date"):
            dd = t.get("due_date")
            if isinstance(dd, date):
                if upcoming is None or dd < upcoming:
                    upcoming = dd
    return {"total": total, "by_status": by_status, "next_due": upcoming}


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = _tasks.get(task_id)
    if not task or task.get("owner") != current_user["username"]:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskOut)
def update_task(task_id: int, payload: TaskUpdate, current_user: dict = Depends(get_current_user)):
    task = _tasks.get(task_id)
    if not task or task.get("owner") != current_user["username"]:
        raise HTTPException(status_code=404, detail="Task not found")
    if payload.title is not None:
        task["title"] = payload.title
    if payload.description is not None:
        task["description"] = payload.description
    if payload.due_date is not None:
        task["due_date"] = payload.due_date
    if payload.status is not None:
        task["status"] = payload.status
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: dict = Depends(get_current_user)):
    task = _tasks.get(task_id)
    if task and task.get("owner") == current_user["username"]:
        del _tasks[task_id]
        return {"deleted": True}
    raise HTTPException(status_code=404, detail="Task not found")


@router.get("/dashboard")
def dashboard(current_user: dict = Depends(get_current_user)):
    # simple dashboard counts
    tasks = [t for t in _tasks.values() if t.get("owner") == current_user["username"]]
    total = len(tasks)
    by_status = {s.value: 0 for s in TaskStatus}
    upcoming = None
    for t in tasks:
        by_status[t["status"].value if hasattr(t["status"], "value") else t["status"]] += 1
        if t.get("due_date"):
            dd = t.get("due_date")
            if isinstance(dd, date):
                if upcoming is None or dd < upcoming:
                    upcoming = dd
    return {"total": total, "by_status": by_status, "next_due": upcoming}
