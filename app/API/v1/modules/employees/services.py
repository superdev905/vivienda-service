from datetime import datetime
from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.elements import and_
from app.settings import SERVICES
