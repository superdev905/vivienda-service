from fastapi import APIRouter
from fastapi.param_functions import Depends
from .middlewares.auth import JWTBearer

from .modules.agreements.routes import router as agreements_router, stat_router
from .modules.employees.routes import router as employees_router
from .modules.phases.routes import router as phase_router


router = APIRouter(dependencies=[Depends(JWTBearer())])

router.include_router(agreements_router)
router.include_router(employees_router)
router.include_router(phase_router)
router.include_router(stat_router)
