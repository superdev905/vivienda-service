from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class Employee(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "employee"
    employee_id = Column(Integer, primary_key=True,
                         unique=True, nullable=False)
    employee_rut = Column(String(12), unique=True, nullable=False)
    fullname = Column(String(200), nullable=False)
    annexed_id = Column(Integer, ForeignKey(
        "agreement_annexed.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    annexed = relationship(
        "AgreementAnnexed", back_populates="employees", lazy="select")
    savings = relationship(
        "EmployeeSaving", back_populates="employee", lazy="select")
    diagnostics = relationship(
        "EmployeeDiagnostic", back_populates="employee", lazy="select")
    phases = relationship(
        "EmployeePhase", back_populates="employee", lazy="select")


class EmployeeSaving(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "employee_saving"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    entity = Column(String(30), nullable=False)
    account_number = Column(String(50), nullable=False)
    amount = Column(Float,  nullable=False)
    employee_id = Column(Integer, ForeignKey(
        "employee.employee_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    employee = relationship(
        "Employee", back_populates="savings", lazy="select")


class EmployeeDiagnostic(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "employee_diagnostic"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    rsh = Column(String(120))
    rsh_id = Column(Integer, nullable=False)
    commune = Column(String(120))
    commune_id = Column(Integer, nullable=False)
    current_subsidy = Column(String(150), nullable=False)
    target_subsidy = Column(String(150), nullable=False)
    atc = Column(String(2), nullable=False)
    disability = Column(String(2), nullable=False)
    marital_status_id = Column(Integer, nullable=False)
    salary = Column(Float,  nullable=False)
    contract_type = Column(String(50),  nullable=False)
    employee_id = Column(Integer, ForeignKey(
        "employee.employee_id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    employee = relationship(
        "Employee", back_populates="diagnostics", lazy="select")
