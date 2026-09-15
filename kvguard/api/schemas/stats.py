"""API Request and Response schemas for stats and metrics."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from kvguard.core.models import CostBreakdown, GPUStats, RequestStats


class HealthResponse(BaseModel):
    status: str = "ok"
    version: str = "0.1.0"
    mode: str = "simulation"
    engine_healthy: bool = True
    metadata_store_healthy: bool = True


class StatsOverviewResponse(BaseModel):
    gpu_stats: GPUStats
    cache_stats: Dict[str, Any]
    active_requests: int = 0
    total_blocks_tracked: int = 0
    cache_hit_rate: float = 0.0
    recent_requests: List[RequestStats] = Field(default_factory=list)
    cost_breakdown: CostBreakdown
