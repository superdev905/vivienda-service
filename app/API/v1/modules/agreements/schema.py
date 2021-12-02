from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import Region, Commune
from ..employees.schema import EmployeeCreate

# id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
# business_id = Column(Integer,  nullable=False)
# business_name = Column(String(120), nullable=False)
# interlocutor_id = Column(Integer, nullable=False)
# interlocutor_name = Column(String(120), nullable=False)
# date = Column(DateTime(timezone=True), nullable=False)
# is_active = Column(Boolean, nullable=False, default=True)
# observations = Column(String(800), nullable=False)


class RelatedBusinessBase(BaseModel):
    business_id: int = Field(alias="businessId")
    business_name: str = Field(alias="businessName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RelatedBusinessCreate(RelatedBusinessBase):
    pass


class ProfessionalBase(BaseModel):
    user_id: int = Field(alias="userId")
    fullname: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ProfessionalCreate(ProfessionalBase):
    pass


class AgreementBase(BaseModel):
    date: datetime
    business_id: int = Field(alias="businessId")
    business_name: str = Field(alias="businessName")
    interlocutor_id: int = Field(alias="interlocutorId")
    interlocutor_name: str = Field(alias="interlocutorName")
    observations: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AgreementCreate(AgreementBase):
    employees: List[EmployeeCreate]
    related_businesses: List[RelatedBusinessCreate]
    professionals: List[ProfessionalCreate]
    pass


class AgreementItem(AgreementBase):
    id: int
    is_active: bool = Field(alias="isActive")
    total_employees: int = Field(alias="totalEmployees")

    class Config:
        allow_population_by_field_name = True
