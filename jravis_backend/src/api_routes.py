from fastapi import APIRouter
from router_health import router as health_router
from router_factory import router as factory_router
from router_growth import router as growth_router
from router_files import router as files_router

router = APIRouter()

router.include_router(health_router, prefix="/api", tags=["health"])
router.include_router(factory_router, prefix="/api/factory", tags=["factory"])
router.include_router(growth_router, prefix="/api/growth", tags=["growth"])
router.include_router(files_router, prefix="/files", tags=["files"])
