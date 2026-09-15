"""Telemetry, GPU, Cache, and Request performance endpoints."""

from typing import Any, Dict, List
from fastapi import APIRouter, Depends
from kvguard.api.dependencies import ServiceContainer, get_container
from kvguard.api.schemas.stats import StatsOverviewResponse
from kvguard.core.models import GPUStats, RequestStats

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("", response_model=StatsOverviewResponse)
async def get_stats_overview(container: ServiceContainer = Depends(get_container)) -> StatsOverviewResponse:
    gpu = await container.engine_adapter.get_gpu_stats()
    cache = await container.engine_adapter.get_cache_stats()
    recent = await container.request_tracker.get_recent_requests(limit=10)
    blocks = await container.metadata_repo.list_blocks(limit=1000)

    cached_tokens = sum(r.cached_tokens for r in recent)
    total_tokens = sum(r.prompt_tokens for r in recent)

    cost = container.cost_model.compute_breakdown(
        gpu_stats=gpu,
        cached_tokens=cached_tokens,
        total_tokens=total_tokens,
        saved_gpu_memory_bytes=len(blocks) * 131072,
        is_simulated=container.settings.execution_mode.value == "simulation",
    )

    return StatsOverviewResponse(
        gpu_stats=gpu,
        cache_stats=cache,
        active_requests=int(cache.get("num_requests_running", 0)),
        total_blocks_tracked=len(blocks),
        cache_hit_rate=cache.get("cache_hit_rate", 0.0),
        recent_requests=recent,
        cost_breakdown=cost,
    )


@router.get("/gpu", response_model=GPUStats)
async def get_gpu_stats(container: ServiceContainer = Depends(get_container)) -> GPUStats:
    return await container.engine_adapter.get_gpu_stats()


@router.get("/cache")
async def get_cache_stats(container: ServiceContainer = Depends(get_container)) -> Dict[str, Any]:
    return await container.engine_adapter.get_cache_stats()


@router.get("/requests", response_model=List[RequestStats])
async def get_recent_requests(
    limit: int = 50, container: ServiceContainer = Depends(get_container)
) -> List[RequestStats]:
    return await container.request_tracker.get_recent_requests(limit=limit)
