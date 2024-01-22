from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum as PyEnum


Base = declarative_base()


class TodoState(str, PyEnum):
    completed = "completado"
    pending = "pendiente"


class TodoModel(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String(120), index=True)
    due_date = Column(Date)
    state = Column(Enum(TodoState))
    labels = Column(String)
