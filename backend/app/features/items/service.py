from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.features.items.models import Item
from app.features.items.schemas import ItemCreate, ItemUpdate


class ItemService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_items(self, *, skip: int = 0, limit: int = 100) -> list[Item]:
        query = select(Item).order_by(Item.id).offset(skip).limit(limit)
        return list(self.db.scalars(query))

    def get_item(self, item_id: int) -> Item:
        item = self.db.get(Item, item_id)
        if item is None:
            raise NotFoundError(f"Item {item_id} not found")
        return item

    def create_item(self, data: ItemCreate) -> Item:
        item = Item(**data.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, item_id: int, data: ItemUpdate) -> Item:
        item = self.get_item(item_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(item, field, value)
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item_id: int) -> None:
        item = self.get_item(item_id)
        self.db.delete(item)
        self.db.commit()
