"""Health check endpoints."""

from fastapi import APIRouter, Depends
from kvguard.api.dependencies import ServiceContainer, get_container
from kvguard.api.schemas.stats import HealthResponse
from kvguard.version import __version__

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(container: ServiceContainer = Depends(get_container)) -> HealthResponse:
    engine_ok = await container.engine_adapter.health()
    return HealthResponse(
        status="ok" if engine_ok else "degraded",
        version=__version__,
        mode=container.settings.execution_mode.value,
        engine_healthy=engine_ok,
        metadata_store_healthy=True,
    )
