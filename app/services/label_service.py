from fastapi import status, HTTPException
from sqlalchemy.orm import Session
from app.database.database import engine
from app.models.todo_model import LabelModel
from app.schemas.label_schema import LabelCreate, LabelUpdate
from sqlalchemy import update, delete, insert


def get_label(
    label_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    label_by_id = session.query(LabelModel).get(label_id)
    if not label_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Label with id {label_id} not found",
        )

    return label_by_id


def get_labels(
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    labels_list = session.query(LabelModel).all()

    if not labels_list:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No labels found"
        )

    return labels_list


def create_label(
    label: LabelCreate, session: Session = Session(bind=engine, expire_on_commit=False)
):
    stmt = insert(LabelModel).values(
        name=label.name,
    )
    session.execute(stmt)
    session.commit()

    retrieved_label = session.query(LabelModel).order_by(LabelModel.id.desc()).first()

    return retrieved_label


def update_label(
    label: LabelUpdate,
    label_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    label_to_update = session.query(LabelModel).get(label_id)

    if not label_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Label with id {label_id} not found",
        )

    stmt = (
        update(LabelModel)
        .where(LabelModel.id == label_id)
        .values(
            name=label.name,
        )
    )
    session.execute(stmt)
    session.commit()

    session.refresh(label_to_update)

    return label_to_update


def delete_label(
    label_id: int,
    session: Session = Session(bind=engine, expire_on_commit=False),
):
    label_to_delete = session.query(LabelModel).get(label_id)

    if label_to_delete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Label with id {label_id} not found",
        )

    label_to_delete.todos.clear()
    stmt = delete(LabelModel).where(LabelModel.id == label_id)
    session.execute(stmt)
    session.commit()
    return f"Label with id {label_id} deleted successfully."
