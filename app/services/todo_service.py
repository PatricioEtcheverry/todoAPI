from typing import Optional, List
from fastapi import HTTPException, Header, status
from app.models.todo_model import TodoState, TodoModel
from app.database.database import engine
from sqlalchemy.orm import Session


def authCheck(X_movitronics: str = Header(...)):
    if X_movitronics != "movietronics_secret_api_key":
        raise HTTPException(status_code=401, detail="Unauthorized")


def format_labels_for_db(labels: List[str]):
    return " - ".join(labels) if labels else "-"


def format_labels_for_response(labels: str):
    return (
        [label.strip() for label in labels.split("-")]
        if "-" in labels
        else [labels.strip()]
    )


# ✅
def get_todo(
    todo_id: int,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)
    todo = session.query(TodoModel).get(todo_id)

    session.close()

    if not todo:
        raise HTTPException(
            status_code=404, detail=f"Todo item with id {todo_id} not found"
        )

    if todo.labels is not None and todo.labels != "-":
        todo.labels = format_labels_for_response(todo.labels)
    else:
        todo.labels = []

    return todo


# ✅
def get_todos(
    state: Optional[str] = None,
    due_date: Optional[str] = None,
    labels: List[str] = None,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)
    todo_list = session.query(TodoModel).all()

    session.close()
    # No se hace mas!!!!
    for todo in todo_list:
        if todo.labels is not None and todo.labels != "-":
            todo.labels = format_labels_for_response(todo.labels)
        else:
            todo.labels = []

    if state:
        todo_list = [todo for todo in todo_list if todo.state == state]
    if due_date:
        todo_list = [todo for todo in todo_list if todo.due_date == due_date]
    if labels:
        todo_list = [
            todo for todo in todo_list if any(label in todo.labels for label in labels)
        ]

    if len(todo_list) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No todos found"
        )
    return todo_list


# ✅
def create_todo(
    todo_data: dict,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)
    todo_to_create = TodoModel(
        name=todo_data.name,
        description=todo_data.description,
        due_date=todo_data.due_date,
        state=TodoState.pending,
        labels="-",
    )

    session.add(todo_to_create)
    session.commit()
    retrieved_todo = session.query(TodoModel).order_by(TodoModel.id.desc()).first()

    session.close()
    if retrieved_todo:
        retrieved_todo.labels = []

    return retrieved_todo


# ✅
def update_todo(
    todo_id: int,
    update_data: dict,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)

    todo_to_update = session.query(TodoModel).get(todo_id)

    if todo_to_update:
        todo_to_update.description = update_data.description
        todo_to_update.due_date = update_data.due_date
        todo_to_update.state = update_data.state
        todo_to_update.labels = format_labels_for_db(update_data.labels)
        session.commit()
        session.refresh(todo_to_update)
        session.close()

    if not todo_to_update:
        raise HTTPException(
            status_code=404, detail=f"Todo item with id {todo_id} not found"
        )

    if todo_to_update.labels is not None and todo_to_update.labels != "-":
        todo_to_update.labels = format_labels_for_response(todo_to_update.labels)
    else:
        todo_to_update.labels = []

    return todo_to_update


# ✅
def complete_todo(
    todo_id: int,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)

    todo_to_complete = session.query(TodoModel).get(todo_id)

    if todo_to_complete:
        if todo_to_complete.state == TodoState.completed:
            raise HTTPException(
                status_code=400, detail="The todo item is already completed"
            )
        todo_to_complete.state = TodoState.completed
        session.commit()
        session.refresh(todo_to_complete)
        session.close()

    if not todo_to_complete:
        raise HTTPException(
            status_code=404, detail=f"Todo item with id {todo_id} not found"
        )

    return f"Todo with id {todo_id} completed successfully."


# ✅
def delete_todo(
    todo_id: int,
    X_movitronics: str = Header(...),
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    authCheck(X_movitronics)

    todo_to_delete = session.query(TodoModel).get(todo_id)

    if todo_to_delete:
        session.delete(todo_to_delete)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"Todo with id {todo_id} not found")

    return f"Todo with id {todo_id} deleted successfully."
