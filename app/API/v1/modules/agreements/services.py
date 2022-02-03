
from datetime import datetime
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from app.database.base import Base
from ..phases.services import create_phases
from .model import AgreementAnnexed, Professional, RelatedBusiness
from ..employees.model import Employee


def create_annexed(db: Session, data, agreement_id: int, user_id: int, date: datetime):
    employees = data.employees
    professionals = data.professionals
    related_businesses = data.related_businesses

    new_annexed = jsonable_encoder(data, by_alias=False)
    del new_annexed["employees"]
    del new_annexed["professionals"]
    del new_annexed["related_businesses"]
    new_annexed["created_by"] = user_id
    new_annexed["agreement_id"] = agreement_id
    new_annexed["date"] = date
    new_annexed["total_employees"] = len(employees)

    db_annexed = AgreementAnnexed(**new_annexed)
    db.add(db_annexed)
    db.commit()
    db.refresh(db_annexed)

    create_employees(db, Employee, employees, db_annexed.id, user_id)
    create_items(db, Professional, professionals, db_annexed.id, user_id)
    create_items(db, RelatedBusiness, related_businesses,
                 db_annexed.id, user_id)


def create_items(db: Session, Model: Base, list: List, annexed_id: int, user_id: int):
    for item in list:
        new_item = jsonable_encoder(item, by_alias=False)
        new_item["created_by"] = user_id
        new_item["annexed_id"] = annexed_id

        db_item = Model(**new_item)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)


def create_employees(db: Session, Model: Base, list: List, annexed_id: int, user_id: int):
    for item in list:

        doc = None
        emp = db.query(Model).filter(
            Model.employee_id == item.employee_id).first()

        if not emp:

            new_item = jsonable_encoder(item, by_alias=False)
            new_item["created_by"] = user_id
            new_item["annexed_id"] = annexed_id

            db_item = Model(**new_item)

            db.add(db_item)
            db.commit()
            db.refresh(db_item)

            doc = db_item
        else:
            doc = emp

        create_phases(db, doc.employee_id, user_id)
