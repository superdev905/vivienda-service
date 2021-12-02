
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from app.database.base import Base
from app.settings import SERVICES
from ..employees.model import Employee


def create_items(db: Session, Model: Base, list: List, agreement_id: int, user_id: int):
    for item in list:
        new_item = jsonable_encoder(item, by_alias=False)
        new_item["created_by"] = user_id
        new_item["agreement_id"] = agreement_id

        db_item = Model(**new_item)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
