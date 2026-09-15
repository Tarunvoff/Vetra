"""Prefetch planning and schedule generation."""

from typing import Any, Dict, List
from vetra.core.enums import CacheLocation, DecisionType
from vetra.core.models import KVBlockStats, Recommendation
from vetra.policy.recommendation import build_recommendation


class PrefetchPlanner:
    """Predicts sequential prefix reuse and schedules asynchronous transfers."""

    def predict_next_blocks(self, current_block: KVBlockStats, all_blocks: List[KVBlockStats]) -> List[KVBlockStats]:
        """Predict likely next blocks in a multi-turn conversation or RAG sequence."""
        if not current_block.session_id:
            return []

        # Find blocks in the same session created after this block
        candidates = [
            b for b in all_blocks
            if b.session_id == current_block.session_id and b.block_id != current_block.block_id
        ]
        candidates.sort(key=lambda b: b.created_at)
        return candidates[:3]

    def generate_prefetch_plan(self, cpu_blocks: List[KVBlockStats]) -> List[Recommendation]:
        """Generate recommendations to prefetch high-value CPU blocks to GPU."""
        plan: List[Recommendation] = []
        for block in cpu_blocks:
            if block.location == CacheLocation.CPU and block.importance_score >= 0.70:
                rec = build_recommendation(
                    block=block,
                    decision=DecisionType.PREFETCH,
                    importance=block.importance_score,
                    reason="High reuse probability on CPU resident block; prefetch to eliminate TTFT penalty.",
                )
                plan.append(rec)
        return plan

    def estimate_prefetch_cost(self, num_blocks: int, bytes_per_block: int = 131072) -> Dict[str, Any]:
        total_bytes = num_blocks * bytes_per_block
        # PCIe 4.0 x16 theoretical throughput ~25 GB/s
        transfer_time_ms = (total_bytes / (25 * 1024 * 1024 * 1024)) * 1000.0
        return {
            "num_blocks": num_blocks,
            "total_bytes": total_bytes,
            "estimated_transfer_time_ms": round(transfer_time_ms, 3),
        }
