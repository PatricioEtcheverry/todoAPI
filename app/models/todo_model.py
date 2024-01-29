from sqlalchemy import Column, Integer, String, Date, Enum, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship

Base = declarative_base()


class TodoState(str, PyEnum):
    pending = "pendiente"
    completed = "completado"


todo_label_association = Table(
    "todo_label_association",
    Base.metadata,
    Column("todo_id", ForeignKey("todos.id"), primary_key=True),
    Column("label_id", ForeignKey("labels.id"), primary_key=True),
)

class LabelModel(Base):
    __tablename__ = "labels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True)
    todos = relationship("TodoModel", secondary=todo_label_association, back_populates="labels")

class TodoModel(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String(120), index=True)
    due_date = Column(Date)
    state = Column(Enum(TodoState), default=TodoState.pending)
    labels = relationship("LabelModel", secondary=todo_label_association, back_populates="todos")
