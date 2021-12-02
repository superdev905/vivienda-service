from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from pydantic.errors import EmailError
from sqlalchemy.orm import relationship


class SuccessResponse(BaseModel):
    message: str


class User (BaseModel):
    id: int
    names: str
    paternal_surname: str = Field(alias='paternalSurname')
    maternal_surname: str = Field(alias='maternalSurname')


class PaginationResponse (BaseModel):
    page: int
    size: int
    total: int


class EmployeeResponse(BaseModel):
    run: str
    id: int
    names: str
    paternal_surname: str = Field(alias="paternalSurname")
    maternal_surname: str = Field(alias="maternalSurname")
    gender: str

    class Config:
        allow_population_by_field_name = True


class BussinessResponse(BaseModel):
    rut: str
    id: int
    address: str
    email: str
    business_name: str = Field(alias="businessName")

    class Config:
        allow_population_by_field_name = True


class BeneficiaryResponse(BaseModel):
    run: Optional[str]
    id: int
    names: str
    relationship: Optional[str]
    is_relative: bool = Field(alias="isRelative")
    paternal_surname: str = Field(alias="paternalSurname")
    maternal_surname: str = Field(alias="maternalSurname")

    class Config:
        allow_population_by_field_name = True


class Region(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Commune(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Otec(BaseModel):
    business_name: str = Field(alias="businessName")
    rut: str
    address: str
    latitude: float
    longitude: float
    region_id: int = Field(alias="regionId")
    commune_id: int = Field(alias="communeId")
    phone: Optional[str]
    email: str
    contact: str
    id: int
    region: Region
    commune: Commune


class Attachment (BaseModel):
    file_name: str = Field(alias="fileName")
    file_key: str = Field(alias="fileKey")
    file_url: str = Field(alias="fileUrl")
    file_size: str = Field(alias="fileSize")
    upload_date: datetime = Field(alias="uploadDate")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CourseDetails(BaseModel):
    code: str
    name: str
    create_date: datetime = Field(alias="createDate")
    otec_id: Optional[int] = Field(alias="otecId")
    instructor_id: int = Field(alias="instructorId")
    description: str
    benefit_id: int = Field(alias="benefitId")
    id: int
    state: str
    created_by: User = Field(alias="createdBy")
    instructor: Optional[User] = Field(alias="instructor")
    otec: Optional[Otec]
    time_ago: str = Field(alias="timeAgo")

    class Config:
        allow_population_by_field_name = True
