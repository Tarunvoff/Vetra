"""CPU host memory placement evaluator."""

from kvguard.core.enums import CacheLocation
from kvguard.core.models import KVBlockStats, PlacementDecision


def evaluate_cpu_tier(block: KVBlockStats, importance: float, cpu_pressure: float = 0.4) -> PlacementDecision:
    """Evaluate placement on CPU host RAM."""
    if cpu_pressure < 0.85:
        return PlacementDecision(
            block_id=block.block_id,
            target_location=CacheLocation.CPU,
            score=importance,
            estimated_transfer_time_ms=10.0,
            reason="Suitable candidate for intermediate CPU host tier.",
        )
    return PlacementDecision(
        block_id=block.block_id,
        target_location=CacheLocation.REMOTE,
        score=importance,
        estimated_transfer_time_ms=45.0,
        reason="CPU RAM saturated; tiering to remote storage.",
    )
