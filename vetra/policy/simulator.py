"""Offline policy simulator running recommendations over block collections."""

from typing import List
from vetra.core.models import GPUStats, KVBlockStats, Recommendation
from vetra.policy.engine import PolicyEngine
from vetra.scoring.importance import compute_importance


class PolicySimulator:
    """Simulates policy decisions across a batch of KV blocks."""

    def __init__(self, policy_engine: PolicyEngine | None = None) -> None:
        self.engine = policy_engine or PolicyEngine()

    def simulate_batch(
        self,
        blocks: List[KVBlockStats],
        gpu_stats: GPUStats,
    ) -> List[Recommendation]:
        recommendations: List[Recommendation] = []
        for block in blocks:
            importance = compute_importance(block)
            rec = self.engine.evaluate(block, gpu_stats, importance)
            recommendations.append(rec)
        return recommendations
