from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm.session import Session
from .model import EmployeePhase

DEFAULT_PHASES = [{"name": "BONO ARRIENDO", "level": 1},
                  {"name": "AHORRO", "level": 2},
                  {"name": "POSTULACIÓN", "level": 3},
                  {"name": "OBTENCIÓN SUBSIDIO", "level": 4},
                  {"name": "BUSQUEDA VIVIENDA", "level": 5},
                  {"name": "CRÉDITO", "level": 6},
                  {"name": "ESCRITURACIÓN", "level": 7},
                  {"name": "PROPIETARIO", "level": 8}]


def create_phases(db: Session, employee_id: int, user_id: int):
    for phase in DEFAULT_PHASES:
        employee_phase = jsonable_encoder(phase)
        employee_phase["created_by"] = user_id
        employee_phase["employee_id"] = employee_id
        employee_phase["status"] = "PENDIENTE"
        employee_phase["is_locked"] = False if phase["name"] == "AHORRO" else True

        db_phase = EmployeePhase(**employee_phase)

        db.add(db_phase)
        db.commit()
        db.refresh(db_phase)
