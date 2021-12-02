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
from .model import Employee

router = APIRouter(prefix="/employee",
                   tags=["Trabajadores"],
                   dependencies=[Depends(JWTBearer())])


# @router.post("", response_model=ScheduleItem)
# def create(req: Request,
#            body: ScheduleCreate,
#            db: Session = Depends(get_database)):
#     new_schedule = jsonable_encoder(body, by_alias=False)
#     new_schedule["created_by"] = req.user_id
#     db_schedule = Schedule(**new_schedule)
#     db.add(db_schedule)
#     db.commit()
#     db.refresh(db_schedule)
#     return db_schedule
