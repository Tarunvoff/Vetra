"""Hierarchical placement planner coordinating GPU, CPU, Remote, and Eviction tiers."""

from vetra.core.enums import CacheLocation
from vetra.core.interfaces import IPlacementPlanner
from vetra.core.models import GPUStats, KVBlockStats, PlacementDecision
from vetra.placement.cpu import evaluate_cpu_tier
from vetra.placement.gpu import evaluate_gpu_tier
from vetra.placement.remote import evaluate_remote_tier


class PlacementPlanner(IPlacementPlanner):
    """Multi-tiered placement engine planning location transitions."""

    def plan_placement(
        self,
        block: KVBlockStats,
        gpu_stats: GPUStats,
        importance: float,
        reuse_prob: float,
    ) -> PlacementDecision:
        combined_score = (importance * 0.6) + (reuse_prob * 0.4)

        if gpu_stats.memory_pressure < 0.80 or combined_score >= 0.70:
            return evaluate_gpu_tier(block, gpu_stats, combined_score)
        elif combined_score >= 0.30:
            return evaluate_cpu_tier(block, combined_score)
        else:
            return evaluate_remote_tier(block, combined_score)
