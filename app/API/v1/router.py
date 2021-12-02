from fastapi import APIRouter
from fastapi.param_functions import Depends
from .middlewares.auth import JWTBearer

from .modules.agreements.routes import router as agreements_router


router = APIRouter(dependencies=[Depends(JWTBearer())])

router.include_router(agreements_router)
# router.include_router(meetings_router)
