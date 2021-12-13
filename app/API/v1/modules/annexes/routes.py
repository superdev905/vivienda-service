from sqlalchemy.sql.elements import and_
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_users_service
from .schema import AnnexedCreateAgreement, AnnexedDetails, AnnexedItem
from .services import create_annexed, create_phases, AgreementAnnexed
from ..employees.model import Employee
from ..employees.schema import EmployeeCreate, EmployeeItem


router = APIRouter(prefix="/annexes",
                   tags=["Convenios"],
                   dependencies=[Depends(JWTBearer())])


@router.post("/{id}/validate", response_model=AnnexedItem)
def validate(req: Request,
             id: int,
             db: Session = Depends(get_database)):
    found_annexed = db.query(AgreementAnnexed).filter(
        AgreementAnnexed.id == id).first()

    if not found_annexed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un anexo con este id: %s".format(id))

    found_annexed.state = "VALID"
    db.add(found_annexed)
    db.commit()
    db.refresh(found_annexed)

    return found_annexed


@router.post("/{id}/employee", response_model=EmployeeItem)
def add_employee(req: Request,
                 id: int,
                 body: EmployeeCreate,
                 db: Session = Depends(get_database)):
    found_annexed = db.query(AgreementAnnexed).filter(
        AgreementAnnexed.id == id).first()

    if not found_annexed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un anexo con este id: %s".format(id))

    found_employee = db.query(Employee).filter(and_(
        Employee.annexed_id == id, Employee.employee_id == body.employee_id)).first()

    if found_employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Este empleado ya esta agregado en este convenio")

    new_employee = jsonable_encoder(body, by_alias=False)
    new_employee["created_by"] = req.user_id
    new_employee["annexed_id"] = id
    db_employee = Employee(**new_employee)

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    create_phases(db, db_employee.id, req.user_id)

    return db_employee


@router.get("/{id}", response_model=AnnexedDetails)
def get_one(req: Request,
            id: int,
            db: Session = Depends(get_database)):
    found_annexed = db.query(AgreementAnnexed).filter(AgreementAnnexed.id == id).options(
        joinedload(AgreementAnnexed.professionals), joinedload(AgreementAnnexed.related_businesses)).first()

    if not found_annexed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un anexo con este id: %s".format(id))
    author = fetch_users_service(req.token, found_annexed.created_by)

    return {**found_annexed.__dict__,
            "author": author, }


@router.post("", response_model=AnnexedItem)
def create(req: Request,
           body: AnnexedCreateAgreement,
           db: Session = Depends(get_database)):
    user_id = req.user_id
    dirty_body = jsonable_encoder(body, by_alias=False)
    clean_body = body
    del clean_body.agreement_id

    annexed = create_annexed(
        db, clean_body, dirty_body["agreement_id"], user_id, body.date)

    return annexed
