from pydantic import BaseModel, constr
from datetime import date
from app.models.todo_model import TodoState
from typing import List
from app.schemas.label_schema import Label, LabelUpdate, LabelCreate


class Todo(BaseModel):
    id: int
    name: str
    description: constr(max_length=120)
    due_date: date
    state: TodoState
    labels: List[Label] = []

    class Config:
        orm_mode = True


class PostTodos(BaseModel):
    name: str
    description: constr(max_length=120)
    due_date: date | None = None
    labels: List[LabelCreate] | None = None


class UpdateTodos(BaseModel):
    description: constr(max_length=120) | None = None
    due_date: date | None = None
    state: TodoState | None = None
    labels: List[LabelUpdate] | None = None
