"""Optimization strategies: quantization, prefetching, offloading, memory budgets, and SLOs."""

from vetra.optimization.cost import CostAwareOptimizer
from vetra.optimization.latency import LatencyOptimizer
from vetra.optimization.memory import MemoryBudgetOptimizer
from vetra.optimization.offloading import OffloadingOptimizer
from vetra.optimization.prefetch import PrefetchPlanner
from vetra.optimization.quantization import QuantizationStrategy
from vetra.optimization.slo import SLOMonitor

__all__ = [
    "QuantizationStrategy",
    "PrefetchPlanner",
    "OffloadingOptimizer",
    "MemoryBudgetOptimizer",
    "LatencyOptimizer",
    "CostAwareOptimizer",
    "SLOMonitor",
]
