from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

# employee_id = Column(Integer, nullable=False)
# fullname = Column(String(200), nullable=False)


class EmployeeBase(BaseModel):
    employee_id: int = Field(alias="employeeId")
    fullname: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class EmployeeCreate(EmployeeBase):
    pass
