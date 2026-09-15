"""Policy constraint validator and evaluator."""

from vetra.core.models import GPUStats, PolicyConstraints


class PolicyConstraintChecker:
    """Evaluates whether current execution context violates operational constraints."""

    @staticmethod
    def is_gpu_over_threshold(gpu_stats: GPUStats, constraints: PolicyConstraints) -> bool:
        """Check if GPU pressure exceeds maximum configured threshold."""
        return gpu_stats.memory_pressure > constraints.max_gpu_memory_percent

    @staticmethod
    def is_importance_below_floor(importance: float, constraints: PolicyConstraints) -> bool:
        """Check if block importance falls below minimum retention floor."""
        return importance < constraints.minimum_block_importance
