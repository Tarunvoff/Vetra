from kvguard.core.models import GPUStats, PolicyConstraints
from kvguard.policy.constraints import PolicyConstraintChecker


def test_gpu_pressure_threshold(high_pressure_gpu_stats: GPUStats):
    constraints = PolicyConstraints(max_gpu_memory_percent=0.85)
    violated = PolicyConstraintChecker.is_gpu_over_threshold(high_pressure_gpu_stats, constraints)
    assert violated is True
