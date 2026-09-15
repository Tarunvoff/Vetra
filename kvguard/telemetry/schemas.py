"""Telemetry snapshot and aggregation schemas."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from kvguard.core.models import GPUStats, RequestStats


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class TelemetrySnapshot(BaseModel):
    """Point-in-time consolidated telemetry snapshot."""

    timestamp: datetime = Field(default_factory=utc_now)
    gpu_stats: GPUStats
    cache_stats: Dict[str, Any] = Field(default_factory=dict)
    active_requests: int = 0
    total_blocks_tracked: int = 0
    cache_hit_rate: float = 0.0
    cache_miss_rate: float = 0.0
    recent_requests: List[RequestStats] = Field(default_factory=list)


class AggregatedMetrics(BaseModel):
    """Aggregated telemetry statistics over a rolling window."""

    window_seconds: float = 60.0
    sample_count: int = 0
    avg_gpu_utilization: float = 0.0
    avg_kv_memory_bytes: float = 0.0
    avg_hit_rate: float = 0.0
    p95_ttft_ms: Optional[float] = None
    p95_latency_ms: Optional[float] = None
    total_tokens_served: int = 0
    total_cached_tokens: int = 0
