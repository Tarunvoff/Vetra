"""Optimization strategies: quantization, prefetching, offloading, memory budgets, and SLOs."""

from kvguard.optimization.cost import CostAwareOptimizer
from kvguard.optimization.latency import LatencyOptimizer
from kvguard.optimization.memory import MemoryBudgetOptimizer
from kvguard.optimization.offloading import OffloadingOptimizer
from kvguard.optimization.prefetch import PrefetchPlanner
from kvguard.optimization.quantization import QuantizationStrategy
from kvguard.optimization.slo import SLOMonitor

__all__ = [
    "QuantizationStrategy",
    "PrefetchPlanner",
    "OffloadingOptimizer",
    "MemoryBudgetOptimizer",
    "LatencyOptimizer",
    "CostAwareOptimizer",
    "SLOMonitor",
]
