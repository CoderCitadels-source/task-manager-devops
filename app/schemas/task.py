from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[TaskStatus] = None


class TaskOut(TaskCreate):
    id: int
    status: TaskStatus = TaskStatus.todo
    owner: Optional[str] = None
