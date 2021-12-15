from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class SavingBase(BaseModel):
    entity: Literal['BANCOS', 'COOPERATIVAS', 'CAJAS DE COMPENSACION']
    account_number: str = Field(alias="accountNumber")
    amount: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class SavingCreate(SavingBase):
    pass


class SavingItem(SavingBase):
    id: int
    is_active: str = Field(alias="isActive")
    created_at: datetime = Field(alias="createdDate")


class DiagnosticBase(BaseModel):
    rsh: Optional[str]
    commune: Optional[str]
    rsh_id: int = Field(alias="rshId")
    commune_id: int = Field(alias="communeId")
    current_subsidy: str = Field(alias="currentSubsidy")
    target_subsidy: str = Field(alias="targetSubsidy")
    atc: str
    disability: str
    marital_status_id: int = Field(alias="maritalStatusId")
    contract_type: str = Field(alias="contractType")
    salary: float

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DiagnosticCreate(DiagnosticBase):
    pass


class DiagnosticItem(DiagnosticBase):
    id: int
    is_active: str = Field(alias="isActive")
    created_at: datetime = Field(alias="createdDate")


class EmployeeBase(BaseModel):
    employee_id: int = Field(alias="employeeId")
    employee_rut: str = Field(alias="employeeRut")
    fullname: str = Field(alias="fullName")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeItem(EmployeeBase):
    is_active: str = Field(alias="isActive")
    created_at: datetime = Field(alias="createdDate")


class EmployeeDetails(EmployeeItem):
    saving: Optional[SavingItem]
    diagnostic: Optional[DiagnosticItem]
