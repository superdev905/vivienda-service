from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import Region, Commune, User, BussinessResponse
from ..employees.schema import EmployeeCreate


class RelatedBusinessBase(BaseModel):
    business_id: int = Field(alias="businessId")
    business_name: str = Field(alias="businessName")
    business_rut: str = Field(alias="businessRut")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class RelatedBusinessCreate(RelatedBusinessBase):
    pass


class ProfessionalBase(BaseModel):
    user_id: int = Field(alias="userId")
    fullname: str = Field(alias="fullName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ProfessionalCreate(ProfessionalBase):
    pass


class AgreementBase(BaseModel):
    date: datetime
    number: str
    business_id: int = Field(alias="businessId")
    business_name: str = Field(alias="businessName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AnnexedBase(BaseModel):
    employees: List[EmployeeCreate]
    related_businesses: List[RelatedBusinessCreate]
    professionals: List[ProfessionalCreate]
    observations: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class AnnexedCreate(AnnexedBase):
    pass


class AnnexedCreateAgreement(AnnexedCreate):
    agreement_id: int = Field(alias="agreementId")
    date: datetime


class AnnexedItem(AnnexedBase):
    id: int
    total_employees: int = Field(alias="totalEmployees")
    state: str
    created_at: datetime = Field(alias="createDate")


class AnnexedDetails(AnnexedItem):
    author: User
    employees: Optional[List[EmployeeCreate]]
    professionals: Optional[List[User]]
    related_businesses: Optional[List[BussinessResponse]] = Field(
        alias="relatedBusinesses")
