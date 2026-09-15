"""Benchmark metrics collection and statistical data structures."""

from typing import List, Optional
from pydantic import BaseModel, Field


class BenchmarkMetrics(BaseModel):
    """Execution summary statistics for a benchmark run."""

    mode: str = "baseline"  # baseline vs kvguard
    workload: str = "mixed"
    total_requests: int = 0
    cache_hit_rate: float = 0.0
    avg_ttft_ms: float = 0.0
    p95_ttft_ms: float = 0.0
    throughput_tokens_sec: float = 0.0
    kv_memory_gb: float = 0.0
    gpu_memory_gb: float = 0.0
    estimated_cost_per_hour_usd: float = 2.50
    memory_saved_gb: float = 0.0
    is_simulation: bool = True
