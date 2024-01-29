from fastapi import APIRouter, Query, Path, status
from typing import Optional, List
from datetime import date
from ..services import todo_service
from ..schemas.todo_schema import (
    Todo as TodoSchema,
    PostTodos as PostTodosSchema,
    UpdateTodos as UpdateTodosSchema,
)
from ..models.todo_model import TodoState as TodoStateModel

router = APIRouter()


@router.get("/todos/{todo_id}", tags=["Todos"])
def get_todo(
    todo_id: int = Path(..., gt=0),
) -> TodoSchema:
    return todo_service.get_todo(
        todo_id,
    )


@router.get("/todos", tags=["Todos"])
def get_todos(
    state: Optional[TodoStateModel] = Query(
        None, enum=[state.value for state in TodoStateModel]
    ),
    due_date: Optional[date] = Query(None),
    labels: List[str] = Query(None),
) -> List[TodoSchema]:
    return todo_service.get_todos(state, due_date, labels)


@router.post("/todos", tags=["Todos"], status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_data: PostTodosSchema,
) -> TodoSchema:
    return todo_service.create_todo(
        todo_data,
    )


@router.patch("/todos/{todo_id}", tags=["Todos"])
def update_todo(
    update_data: UpdateTodosSchema,
    todo_id: int = Path(..., gt=0),
) -> TodoSchema:
    return todo_service.update_todo(
        todo_id,
        update_data,
    )


@router.patch("/todos/{todo_id}/complete", tags=["Todos"])
def complete_todo(
    todo_id: int = Path(..., gt=0),
):
    return todo_service.complete_todo(
        todo_id,
    )


@router.delete("/todos/{todo_id}", tags=["Todos"], status_code=status.HTTP_200_OK)
def delete_todo(
    todo_id: int = Path(..., gt=0),
):
    return todo_service.delete_todo(
        todo_id,
    )
