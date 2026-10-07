from fastapi import APIRouter

from backend.api.routes.health import router as health_router
from backend.modules.cases import router as cases_router
from backend.modules.catalogue import router as catalogue_router
from backend.modules.crypto import router as crypto_router
from backend.modules.netscan import router as netscan_router
from backend.modules.planned import router as planned_router
from backend.modules.registry import MODULES
from backend.modules.username import router as username_router
from backend.modules.watchtower import router as watchtower_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(watchtower_router)
api_router.include_router(netscan_router)
api_router.include_router(crypto_router)
api_router.include_router(catalogue_router)
api_router.include_router(username_router)
api_router.include_router(cases_router)
api_router.include_router(planned_router)


@api_router.get("/modules", tags=["system"])
async def modules() -> dict:
    return {"modules": [module.model_dump() for module in MODULES]}
