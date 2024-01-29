from fastapi import APIRouter, status, Path
from app.schemas.label_schema import LabelCreate, LabelUpdate, Label
from ..services import label_service
from typing import List

router = APIRouter()


@router.get("/labels/{label_id}", tags=["Labels"])
def get_label(
    label_id: int = Path(..., gt=0),
) -> Label:
    return label_service.get_label(label_id)


@router.get("/labels", tags=["Labels"])
def get_labels() -> List[Label]:
    return label_service.get_labels()


@router.post("/labels", tags=["Labels"], status_code=status.HTTP_201_CREATED)
def create_label(label: LabelCreate) -> LabelCreate:
    return label_service.create_label(label)


@router.put("/labels/{label_id}", tags=["Labels"], response_model=None)
def update_label(
    label: LabelUpdate,
    label_id: int = Path(..., gt=0),
) -> LabelUpdate:
    return label_service.update_label(label, label_id)


@router.delete(
    "/labels/{label_id}",
    tags=["Labels"],
    status_code=status.HTTP_200_OK,
    response_model=None,
)
def delete_label(label_id: int = Path(..., gt=0)):
    return label_service.delete_label(label_id)
