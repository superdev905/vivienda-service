from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class Employee(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "employee"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    employee_id = Column(Integer, nullable=False)
    fullname = Column(String(200), nullable=False)
    agreement_id = Column(Integer, ForeignKey("agreement.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    agreement = relationship(
        "Agreement", back_populates="employees", lazy="select")
