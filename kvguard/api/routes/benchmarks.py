"""Benchmark status and baseline comparison endpoints."""

from typing import Any, Dict
from fastapi import APIRouter

router = APIRouter(prefix="/benchmarks", tags=["Benchmarks"])


@router.get("")
async def get_benchmarks_overview() -> Dict[str, Any]:
    return {
        "status": "ready",
        "available_workloads": ["multi_turn", "rag", "repeated_prompt", "mixed"],
        "sample_baseline_comparison": {
            "workload": "mixed",
            "metrics": {
                "cache_hit_rate": {"baseline": "42.1%", "kvguard": "67.4%", "delta": "+25.3%"},
                "kv_memory": {"baseline": "11.2 GB", "kvguard": "8.4 GB", "delta": "-25.0%"},
                "ttft_ms": {"baseline": "183 ms", "kvguard": "151 ms", "delta": "-17.5%"},
                "gpu_memory": {"baseline": "18.1 GB", "kvguard": "15.3 GB", "delta": "-15.5%"},
                "cost_per_hour": {"baseline": "$2.50", "kvguard": "$1.95", "delta": "-22.0%"},
            },
            "is_simulation": True,
        },
    }
