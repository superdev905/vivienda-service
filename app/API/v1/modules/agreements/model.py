from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, DateTime
from app.database.base_class import Base, TimestampMixin, AuthorMixin
from sqlalchemy import Column, Integer, String


class Agreement(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "agreement"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    number = Column(String(12), primary_key=True,  nullable=False)
    business_id = Column(Integer,  nullable=False)
    business_name = Column(String(120), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    annexes = relationship(
        "AgreementAnnexed", back_populates="agreement", lazy="select")


class AgreementAnnexed(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "agreement_annexed"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    agreement_id = Column(Integer, ForeignKey(
        "agreement.id"), primary_key=True, nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    state = Column(String(8), nullable=False, default="DRAFT")
    observations = Column(String(800), nullable=False)
    total_employees = Column(Integer, nullable=False)
    employees = relationship(
        "Employee", back_populates="annexed", lazy="select")
    related_businesses = relationship(
        "RelatedBusiness", back_populates="annexed", lazy="select")
    professionals = relationship(
        "Professional", back_populates="annexed", lazy="select")
    agreement = relationship(
        "Agreement", back_populates="annexes", foreign_keys=[agreement_id], lazy="select")


class RelatedBusiness(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "related_business"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    business_id = Column(Integer,  nullable=False)
    business_name = Column(String(120), nullable=False)
    business_rut = Column(String(12), nullable=False)
    annexed_id = Column(Integer, ForeignKey(
        "agreement_annexed.id"), nullable=False)
    annexed = relationship(
        "AgreementAnnexed", back_populates="related_businesses", lazy="select")


class Professional(Base, AuthorMixin, TimestampMixin):
    __tablename__ = "professional"
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(Integer,  nullable=False)
    fullname = Column(String(120), nullable=False)
    annexed_id = Column(Integer, ForeignKey(
        "agreement_annexed.id"), nullable=False)

    annexed = relationship(
        "AgreementAnnexed", back_populates="professionals", lazy="select")
