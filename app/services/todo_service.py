from typing import Optional, List
from fastapi import HTTPException, status
from app.models.todo_model import TodoState, TodoModel, LabelModel
from app.database.database import engine
from sqlalchemy.orm import Session
from sqlalchemy import update, delete, insert


# ✅ ✅ ✅
def get_todo(
    todo_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    todo = session.query(TodoModel).get(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with id {todo_id} not found",
        )

    return todo


# ✅ ✅ ✅
def get_todos(
    state: Optional[str] = None,
    due_date: Optional[str] = None,
    labels: List[str] = None,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    todo_filter_by = session.query(TodoModel)

    if state:
        todo_filter_by = todo_filter_by.filter_by(state=state)
    if due_date:
        todo_filter_by = todo_filter_by.filter_by(due_date=due_date)
    if labels:
        todo_filter_by = todo_filter_by.filter(
            TodoModel.labels.any(LabelModel.name.in_(labels))
        )

    return todo_filter_by


# ✅ ✅ ✅
def create_todo(
    todo_data: dict,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    labels_to_add = []

    for label_data in todo_data.labels:
        existing_label = (
            session.query(LabelModel).filter_by(name=label_data.name).one_or_none()
        )

        print(existing_label)
        if existing_label:
            labels_to_add.append(existing_label)
        else:
            stmt = insert(LabelModel).values(name=label_data.name)
            session.execute(stmt)
            session.commit()
            retrieved_label = (
                session.query(LabelModel).order_by(LabelModel.id.desc()).first()
            )
            labels_to_add.append(retrieved_label)

    create_todo = TodoModel(
        name=todo_data.name,
        description=todo_data.description,
        due_date=todo_data.due_date,
    )
    create_todo.labels.extend(labels_to_add)

    session.add(create_todo)
    session.commit()
    session.refresh(create_todo)

    return create_todo


# ✅ ✅ ✅
def update_todo(
    todo_id: int,
    update_data: dict,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    todo_to_update = session.query(TodoModel).get(todo_id)

    if not todo_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with id {todo_id} not found",
        )

    if update_data.state is not None:
        todo_to_update.state = update_data.state

    if update_data.description is not None:
        todo_to_update.description = update_data.description

    if update_data.due_date is not None:
        todo_to_update.due_date = update_data.due_date

    if update_data.labels is not None:
        updated_labels = []
        for label_data in update_data.labels:
            existing_label = (
                session.query(LabelModel).filter_by(name=label_data.name).one_or_none()
            )

            if existing_label:
                updated_labels.append(existing_label)
            else:
                stmt = insert(LabelModel).values(name=label_data.name)
                session.execute(stmt)
                session.commit()
                retrieved_label = (
                    session.query(LabelModel).order_by(LabelModel.id.desc()).first()
                )
                updated_labels.append(retrieved_label)
        todo_to_update.labels = updated_labels

    session.commit()
    session.refresh(todo_to_update)

    return todo_to_update


# ✅ ✅ ✅
def complete_todo(
    todo_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    todo_to_complete = session.query(TodoModel).get(todo_id)

    if not todo_to_complete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo item with id {todo_id} not found",
        )

    if todo_to_complete.state == TodoState.completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The todo item is already completed",
        )

    stmt = (
        update(TodoModel)
        .where(TodoModel.id == todo_id)
        .values(
            state=TodoState.completed,
        )
    )
    session.execute(stmt)
    session.commit()
    session.refresh(todo_to_complete)

    return f"Todo with id {todo_id} completed successfully."


# ✅ ✅ ✅
def delete_todo(
    todo_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    todo_to_delete = session.query(TodoModel).get(todo_id)

    if todo_to_delete:
        todo_to_delete.labels.clear()
        stmt = delete(TodoModel).where(TodoModel.id == todo_id)
        session.execute(stmt)
        session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    return f"Todo with id {todo_id} deleted successfully."
