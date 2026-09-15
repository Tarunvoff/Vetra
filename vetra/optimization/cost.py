"""Cost-aware optimization and trade-offs."""

from typing import Dict
from vetra.core.models import CostBreakdown, GPUStats
from vetra.economics.cost_model import CostModel


class CostAwareOptimizer:
    """Balances cache retention costs against compute regeneration costs."""

    def __init__(self, cost_model: CostModel | None = None) -> None:
        self.cost_model = cost_model or CostModel()

    def should_offload_or_evict(
        self,
        gpu_stats: GPUStats,
        block_importance: float,
        block_size_bytes: int,
    ) -> str:
        if gpu_stats.memory_pressure > 0.85:
            if block_importance > 0.40:
                return "OFFLOAD_CPU"
            return "EVICT"
        return "KEEP"
