from pydantic import BaseModel


class LabelBase(BaseModel):
    name: str


class LabelCreate(LabelBase):
    pass


class LabelUpdate(LabelBase):
    pass


class Label(LabelBase):
    id: int

    class Config:
        from_attributes = True
