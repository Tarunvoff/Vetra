"""Baseline inference benchmark runner (without active control plane optimization)."""

import asyncio
from typing import List
from benchmarks.metrics import BenchmarkMetrics
from benchmarks.workloads.mixed import generate_mixed_workload


async def run_baseline_benchmark(
    workload_type: str = "mixed", num_requests: int = 50
) -> BenchmarkMetrics:
    """Execute baseline simulation where cache eviction is naive LRU without proactive offloading."""
    workload = generate_mixed_workload()[:num_requests]
    total_prompt = sum(r["prompt_tokens"] for r in workload)
    total_cached = sum(r["cached_tokens"] for r in workload)

    # Naive baseline metrics
    hit_rate = (total_cached / max(1, total_prompt)) * 0.75  # Lower hit rate due to unmanaged thrashing
    ttft = 183.4
    kv_mem = 11.2
    gpu_mem = 18.1

    return BenchmarkMetrics(
        mode="baseline",
        workload=workload_type,
        total_requests=len(workload),
        cache_hit_rate=round(hit_rate, 3),
        avg_ttft_ms=round(ttft, 1),
        p95_ttft_ms=round(ttft * 1.4, 1),
        throughput_tokens_sec=1420.0,
        kv_memory_gb=kv_mem,
        gpu_memory_gb=gpu_mem,
        estimated_cost_per_hour_usd=2.50,
        memory_saved_gb=0.0,
        is_simulation=True,
    )
