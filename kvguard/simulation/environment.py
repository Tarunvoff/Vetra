"""Simulated policy execution environment."""

from typing import Any, Dict, List
from kvguard.core.models import GPUStats, KVBlockStats, Recommendation
from kvguard.policy.engine import PolicyEngine
from kvguard.scoring.importance import compute_importance
from kvguard.simulation.engine import SimulatedEngineAdapter


class SimulatedPolicyEnvironment:
    """Orchestrates mock telemetry, block generation, and policy evaluation cycles."""

    def __init__(self, base_utilization: float = 0.88) -> None:
        self.adapter = SimulatedEngineAdapter(base_utilization=base_utilization)
        self.policy = PolicyEngine()

    async def step(self) -> Dict[str, Any]:
        """Execute one simulation step producing GPU stats, scored blocks, and recommendations."""
        gpu_stats = await self.adapter.get_gpu_stats()
        blocks = await self.adapter.get_block_stats()
        recommendations: List[Recommendation] = []

        for blk in blocks:
            score = compute_importance(blk)
            blk.importance_score = score
            rec = self.policy.evaluate(blk, gpu_stats, score)
            recommendations.append(rec)

        return {
            "gpu_stats": gpu_stats,
            "total_blocks": len(blocks),
            "recommendations": recommendations,
            "memory_pressure": gpu_stats.memory_pressure,
        }
