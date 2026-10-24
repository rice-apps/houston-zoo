from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.features.items.schemas import ItemCreate, ItemRead, ItemUpdate
from app.features.items.service import ItemService

router = APIRouter(prefix="/items", tags=["items"])


def get_item_service(db: Annotated[Session, Depends(get_db)]) -> ItemService:
    return ItemService(db)


ItemServiceDep = Annotated[ItemService, Depends(get_item_service)]


@router.get("", response_model=list[ItemRead])
def list_items(
    service: ItemServiceDep,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 100,
):
    return service.list_items(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, service: ItemServiceDep):
    return service.get_item(item_id)


@router.post("", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(data: ItemCreate, service: ItemServiceDep):
    return service.create_item(data)


@router.patch("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, data: ItemUpdate, service: ItemServiceDep):
    return service.update_item(item_id, data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, service: ItemServiceDep) -> None:
    service.delete_item(item_id)
