"""Economic cost model computing estimated savings and per-million token costs."""

from __future__ import annotations

from kvguard.core.models import CostBreakdown, GPUStats
from kvguard.economics.gpu_cost import estimate_gpu_hourly_cost
from kvguard.economics.memory_cost import estimate_host_ram_hourly_cost


class CostModel:
    """Configurable infrastructure cost calculation engine."""

    def __init__(
        self,
        gpu_hourly_cost: float = 2.50,
        cpu_hourly_cost: float = 0.40,
        storage_per_gb_month: float = 0.05,
    ) -> None:
        self.gpu_hourly_cost = gpu_hourly_cost
        self.cpu_hourly_cost = cpu_hourly_cost
        self.storage_per_gb_month = storage_per_gb_month

    def compute_breakdown(
        self,
        gpu_stats: GPUStats,
        cached_tokens: int,
        total_tokens: int,
        saved_gpu_memory_bytes: int = 0,
        is_simulated: bool = True,
    ) -> CostBreakdown:
        """Compute estimated infrastructure cost and savings breakdown."""
        gpu_rate = estimate_gpu_hourly_cost(gpu_stats.device_name, self.gpu_hourly_cost)

        # Approximate token throughput per hour
        tokens_per_hour = max(1, total_tokens * 60)  # extrapolated
        cost_per_1m = (gpu_rate / (tokens_per_hour / 1_000_000)) if tokens_per_hour > 0 else 0.0

        # Memory savings calculation
        saved_fraction = (saved_gpu_memory_bytes / max(1, gpu_stats.total_memory_bytes))
        savings_per_hour = min(gpu_rate * 0.4, gpu_rate * saved_fraction)

        return CostBreakdown(
            estimated_cost_per_hour=round(gpu_rate, 4),
            estimated_cost_per_1m_tokens=round(cost_per_1m, 4),
            estimated_gpu_memory_cost=round(gpu_rate * gpu_stats.memory_pressure, 4),
            estimated_cpu_memory_cost=round(self.cpu_hourly_cost * 0.2, 4),
            estimated_savings_per_hour=round(savings_per_hour, 4),
            is_simulated=is_simulated,
        )
