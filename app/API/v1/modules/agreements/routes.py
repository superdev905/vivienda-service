from fastapi import status, Request, APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.param_functions import Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import or_
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
from .schema import AgreementDetails, AgreementItem, AgreementCreate
from .services import create_employees, create_items


stat_router = APIRouter(prefix="/stats",
                        tags=["Estadisticas"],
                        dependencies=[Depends(JWTBearer())])


@stat_router.get("")
def get_stats(db: Session = Depends(get_database)):
    agreements = db.query(Agreement).count()

    return {
        "agreements": agreements,
        "owners": 0,
        "employees": db.query(Employee).count()
    }


router = APIRouter(prefix="/agreements",
                   tags=["Convenios"],
                   dependencies=[Depends(JWTBearer())])


@router.get("", response_model=Page[AgreementItem])
def get_all(req: Request,
            search: str = None,
            db: Session = Depends(get_database),
            pag_params: Params = Depends()):
    filters = []
    if search:
        formatted_search = "{}%".format(search)
        filters.append(Agreement.business_name.ilike(formatted_search))

    return paginate(db.query(Agreement).filter(or_(*filters)).options(joinedload(Agreement.professionals)), pag_params)


@router.get("/{id}", response_model=AgreementDetails)
def get_one(req: Request,
            id: int,
            db: Session = Depends(get_database)):
    found_agreement = db.query(Agreement).filter(Agreement.id == id).options(
        joinedload(Agreement.professionals), joinedload(Agreement.related_businesses)).first()

    if not found_agreement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No existe un convenio con este id: %s".format(id))
    author = fetch_users_service(req.token, found_agreement.created_by)

    business = get_business_data(req, found_agreement.business_id)

    return {**found_agreement.__dict__,
            "author": author,
            "business": business}


@router.post("", response_model=AgreementItem)
def create(req: Request,
           body: AgreementCreate,
           db: Session = Depends(get_database)):
    user_id = req.user_id

    found_agreement = db.query(Agreement).filter(
        Agreement.business_id == body.business_id).first()
    if found_agreement:
        raise HTTPException(
            detail="Esta empresa ya tiene un convenio creado:", status_code=status.HTTP_400_BAD_REQUEST)

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
    create_employees(db, Employee, employees, db_agreement.id, user_id)
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
