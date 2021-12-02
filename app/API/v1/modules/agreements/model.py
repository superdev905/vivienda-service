from sqlalchemy.orm import relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime, Float
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class Agreement(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "agreement"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    business_id = Column(Integer,  nullable=False)
    business_name = Column(String(120), nullable=False)
    interlocutor_id = Column(Integer, nullable=False)
    interlocutor_name = Column(String(120), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    observations = Column(String(800), nullable=False)
    total_employees = Column(Integer, nullable=False)
    employees = relationship(
        "Employee", back_populates="agreement", lazy="select")
    related_businesses = relationship(
        "RelatedBusiness", back_populates="agreement", lazy="select")
    professionals = relationship(
        "Professional", back_populates="agreement", lazy="select")


class RelatedBusiness(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "related_business"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    business_id = Column(Integer,  nullable=False)
    business_name = Column(String(120), nullable=False)
    agreement_id = Column(Integer, ForeignKey("agreement.id"), nullable=False)

    agreement = relationship(
        "Agreement", back_populates="related_businesses", lazy="select")


class Professional(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "professional"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer,  nullable=False)
    fullname = Column(String(120), nullable=False)
    agreement_id = Column(Integer, ForeignKey("agreement.id"), nullable=False)

    agreement = relationship(
        "Agreement", back_populates="professionals", lazy="select")
