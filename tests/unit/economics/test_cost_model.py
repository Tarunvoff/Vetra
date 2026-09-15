from vetra.core.models import GPUStats
from vetra.economics.cost_model import CostModel


def test_cost_model_breakdown(normal_gpu_stats: GPUStats):
    model = CostModel(gpu_hourly_cost=2.50, cpu_hourly_cost=0.40)
    breakdown = model.compute_breakdown(
        gpu_stats=normal_gpu_stats,
        cached_tokens=1000,
        total_tokens=2000,
        saved_gpu_memory_bytes=1048576,
    )
    assert breakdown.estimated_cost_per_hour == 2.50
    assert breakdown.estimated_savings_per_hour >= 0.0
