from typing import Optional
from fastapi import status, Request, APIRouter
from starlette.responses import StreamingResponse
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_, or_
from fastapi_pagination import Params, Page
from fastapi_pagination.ext.sqlalchemy import paginate
from app.database.main import get_database
from app.settings import SERVICES
from ...middlewares.auth import JWTBearer
from ...helpers.fetch_data import fetch_service, fetch_users_service, get_business_data
from ...helpers.crud import get_updated_obj
from ...helpers.humanize_date import get_time_ago
from ...helpers.schema import SuccessResponse
from .model import Agreement, Professional, RelatedBusiness
from ..employees.model import Employee
from .schema import AgreementItem, AgreementCreate
from .services import create_items


router = APIRouter(prefix="/agreement",
                   tags=["Convenios"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[AgreementItem])
def get_all(req: Request,
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):

    return paginate(db.query(Agreement).options(joinedload(Agreement.professionals)), pag_params)


@router.post("", response_model=AgreementItem)
def create(req: Request,
           body: AgreementCreate,
           db: Session = Depends(get_database)):
    user_id = req.user_id

    employees = body.employees
    professionals = body.professionals
    related_businesses = body.related_businesses

    new_agreement = jsonable_encoder(body, by_alias=False)

    del new_agreement["employees"]
    del new_agreement["professionals"]
    del new_agreement["related_businesses"]

    new_agreement["created_by"] = user_id
    new_agreement["total_employees"] = len(employees)
    db_agreement = Agreement(**new_agreement)

    db.add(db_agreement)
    db.commit()
    db.flush(db_agreement)

    create_items(db, Professional, professionals, db_agreement.id, user_id)
    create_items(db, Employee, employees, db_agreement.id, user_id)
    create_items(db, RelatedBusiness, related_businesses,
                 db_agreement.id, user_id)

    return db_agreement


# @router.get("/{id}", response_model=ScheduleDetails)
# def get_one(req: Request,
#             id: int,
#             db: Session = Depends(get_database)):
#     found_schedule = db.query(Schedule).filter(Schedule.id == id).first()

#     if not found_schedule:
#         raise HTTPException(
#             detail="No existe una programación con este id: " + str(id), status_code=status.HTTP_400_BAD_REQUEST)
#     business = get_business_data(req, found_schedule.business_id)
#     boss = fetch_users_service(
#         req.token, found_schedule.boss_id)

#     return {**found_schedule.__dict__,
#             "business": business,
#             "boss": boss}


# @router.get("/{id}/report")
# def generate_report(req: Request,
#                     id: int,
#                     db: Session = Depends(get_database)):
#     found_schedule = db.query(Schedule).filter(Schedule.id == id).first()

#     if not found_schedule:
#         raise HTTPException(
#             detail="No existe una programación con este id: " + str(id), status_code=status.HTTP_400_BAD_REQUEST)
#     business = get_business_data(req, found_schedule.business_id)
#     boss = fetch_users_service(
#         req.token, found_schedule.boss_id)

#     file_name = "2021-IT Process"

#     headers = {
#         'Content-Disposition': "attachment; filename=" + file_name + ".pdf"
#     }

#     attachment = create_schedule_doc()

#     return StreamingResponse(attachment, headers=headers)
