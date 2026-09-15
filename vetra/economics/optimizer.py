"""Economic cost optimizer implementing ICostOptimizer."""

from vetra.core.interfaces import ICostOptimizer
from vetra.core.models import CostBreakdown, GPUStats
from vetra.economics.cost_model import CostModel


class CostOptimizer(ICostOptimizer):
    """Calculates ROI and optimal tiering trade-offs based on economic parameters."""

    def __init__(self, cost_model: CostModel | None = None) -> None:
        self.model = cost_model or CostModel()

    def calculate_cost_breakdown(
        self,
        gpu_stats: GPUStats,
        total_blocks: int,
        cached_tokens: int,
        active_hours: float = 1.0,
    ) -> CostBreakdown:
        saved_bytes = total_blocks * 16 * 128 * 2 * 32  # Estimated saved capacity
        return self.model.compute_breakdown(
            gpu_stats=gpu_stats,
            cached_tokens=cached_tokens,
            total_tokens=cached_tokens * 2,
            saved_gpu_memory_bytes=saved_bytes,
        )
