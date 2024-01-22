from pydantic import BaseModel, constr
from datetime import date
from typing import Optional
from app.models.todo_model import TodoState


class Todo(BaseModel):
    name: str
    description: constr(max_length=120)
    due_date: date
    state: TodoState
    labels: list


class PostTodos(BaseModel):
    name: str
    description: constr(max_length=120)
    due_date: Optional[date]


class UpdateTodos(BaseModel):
    description: Optional[constr(max_length=120)] = None
    due_date: Optional[date] = None
    state: Optional[TodoState] = None
    labels: Optional[list] = None
