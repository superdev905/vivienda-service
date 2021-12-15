from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class EmployeePhase(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "employee_phase"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(20), nullable=False)
    level = Column(Integer, nullable=False)
    status = Column(String(10))
    start_date = Column(DateTime(timezone=True))
    end_date = Column(DateTime(timezone=True))
    employee_id = Column(Integer, ForeignKey(
        "employee.employee_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_locked = Column(Boolean, nullable=False, server_default="0")

    employee = relationship(
        "Employee", back_populates="phases", lazy="select")
