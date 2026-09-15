"""GPU tier placement evaluators."""

from vetra.core.enums import CacheLocation
from vetra.core.models import GPUStats, KVBlockStats, PlacementDecision


def evaluate_gpu_tier(block: KVBlockStats, gpu_stats: GPUStats, importance: float) -> PlacementDecision:
    """Evaluate whether block should reside on high-speed GPU HBM."""
    if gpu_stats.memory_pressure < 0.85 or importance >= 0.70:
        return PlacementDecision(
            block_id=block.block_id,
            target_location=CacheLocation.GPU,
            score=importance,
            estimated_transfer_time_ms=0.0,
            reason="High importance or sufficient GPU headroom available.",
        )
    return PlacementDecision(
        block_id=block.block_id,
        target_location=CacheLocation.CPU,
        score=importance,
        estimated_transfer_time_ms=12.0,
        reason="GPU memory threshold exceeded; recommend host RAM offload.",
    )
