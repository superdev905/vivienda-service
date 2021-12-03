from typing import Optional
from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.main import get_database
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_users_service, get_employee_data
from ...helpers.crud import get_updated_obj
from ...helpers.humanize_date import get_time_ago
from ...helpers.schema import SuccessResponse
from .model import Employee, EmployeeSaving, EmployeeDiagnostic
from .schema import DiagnosticCreate, DiagnosticItem, EmployeeDetails, EmployeeItem, SavingCreate, SavingItem

router = APIRouter(prefix="/employees",
                   tags=["Trabajadores"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[EmployeeItem])
def get_all(search: str = None,
            agreement_id: int = Query(None, alias="agreementId"),
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):

    filters = []
    if search:
        formatted_search = "{}%".format(search)
        filters.append(Employee.fullname.ilike(formatted_search))
    return paginate(db.query(Employee).filter(or_(*filters, Employee.agreement_id == agreement_id)), pag_params)


@router.get("/{id}", response_model=EmployeeDetails)
def get_one(id: int,
            db: Session = Depends(get_database)):

    employee = db.query(Employee).filter(Employee.id == id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un trabajador con este id: %s".format(id))

    saving = db.query(EmployeeSaving).filter(
        and_(EmployeeSaving.employee_id == id, EmployeeSaving.is_active == True)).first()
    diagnostic = db.query(EmployeeDiagnostic).filter(
        and_(EmployeeDiagnostic.employee_id == id, EmployeeDiagnostic.is_active == True)).first()

    return {**employee.__dict__,
            "saving": saving,
            "diagnostic": diagnostic}


@router.post("/{id}/saving", response_model=SavingItem)
def create_saving(req: Request,
                  id: int,
                  body: SavingCreate,
                  db: Session = Depends(get_database)):
    new_saving = jsonable_encoder(body, by_alias=False)
    new_saving["employee_id"] = id
    new_saving["created_by"] = req.user_id

    db_saving = EmployeeSaving(**new_saving)

    db.add(db_saving)
    db.commit()
    db.refresh(db_saving)

    return db_saving


@router.put("/saving/{id}", response_model=SavingItem)
def update_saving(req: Request,
                  id: int,
                  body: SavingCreate,
                  db: Session = Depends(get_database)):
    saving = db.query(EmployeeSaving).filter(EmployeeSaving.id == id).first()

    if not saving:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un convenio con este id: %s".format(id))

    updated_saving = get_updated_obj(saving, body)

    db.add(updated_saving)
    db.commit()
    db.refresh(updated_saving)

    return updated_saving


@router.post("/{id}/diagnostic", response_model=DiagnosticItem)
def create_diagnostic(req: Request,
                      id: int,
                      body: DiagnosticCreate,
                      db: Session = Depends(get_database)):
    new_diagnostic = jsonable_encoder(body, by_alias=False)
    new_diagnostic["employee_id"] = id
    new_diagnostic["created_by"] = req.user_id

    db_diagnostic = EmployeeDiagnostic(**new_diagnostic)

    db.add(db_diagnostic)
    db.commit()
    db.refresh(db_diagnostic)

    return db_diagnostic


@router.put("/diagnostic/{id}", response_model=DiagnosticItem)
def update_saving(req: Request,
                  id: int,
                  body: DiagnosticCreate,
                  db: Session = Depends(get_database)):
    diagnostic = db.query(EmployeeDiagnostic).filter(
        EmployeeDiagnostic.id == id).first()

    if not diagnostic:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un diagnostico con este id: %s".format(id))

    updated_diagnostic = get_updated_obj(diagnostic, body)

    db.add(updated_diagnostic)
    db.commit()
    db.refresh(updated_diagnostic)

    return updated_diagnostic
