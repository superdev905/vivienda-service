from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from ...helpers.schema import User, BussinessResponse
from ..annexes.schema import AnnexedCreate, AnnexedItem


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


class AgreementCreate(AgreementBase):
    annexed: AnnexedCreate
    pass


class AgreementItem(AgreementBase):
    id: int
    is_active: bool = Field(alias="isActive")

    class Config:
        allow_population_by_field_name = True


class AgreementDetails(AgreementItem):
    annexes: Optional[List[AnnexedItem]]
    author: User
    business: BussinessResponse

    class Config:
        allow_population_by_field_name = True
