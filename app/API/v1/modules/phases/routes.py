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
from .model import EmployeePhase
from .schema import PhaseBase, PhaseItem

router = APIRouter(prefix="/employee-phases",
                   tags=["Etapas del proceso"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[PhaseItem])
def get_all(employee_id: int = Query(None, alias="employeeId"),
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):

    return paginate(db.query(EmployeePhase).filter(or_(EmployeePhase.employee_id == employee_id)).order_by(EmployeePhase.created_at), pag_params)


@router.put("/{id}", response_model=PhaseItem)
def update_saving(req: Request,
                  id: int,
                  body: PhaseBase,
                  db: Session = Depends(get_database)):
    phase = db.query(EmployeePhase).filter(EmployeePhase.id == id).first()

    if not phase:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe una etapa con este id: %s".format(id))

    updated_phase = get_updated_obj(phase, body)

    db.add(updated_phase)
    db.commit()
    db.refresh(updated_phase)

    return updated_phase
