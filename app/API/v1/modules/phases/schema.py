from datetime import datetime
from typing import Literal, Optional
from pydantic import BaseModel, Field


class PhaseBase(BaseModel):
    name: str
    level: int
    status: Optional[str]
    start_date: Optional[datetime] = Field(alias="startDate")
    end_date: Optional[datetime] = Field(alias="endDate")
    employee_id: int = Field(alias="employeeId")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PhaseItem(PhaseBase):
    id: int
    is_active: bool = Field(alias="isActive")
    is_locked: bool = Field(alias="isLocked")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
