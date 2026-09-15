"""Remote NVMe / Network storage placement evaluator."""

from kvguard.core.enums import CacheLocation
from kvguard.core.models import KVBlockStats, PlacementDecision


def evaluate_remote_tier(block: KVBlockStats, importance: float) -> PlacementDecision:
    """Evaluate placement on remote NVMe-oF or shared object tier."""
    if importance >= 0.20:
        return PlacementDecision(
            block_id=block.block_id,
            target_location=CacheLocation.REMOTE,
            score=importance,
            estimated_transfer_time_ms=50.0,
            reason="Retaining in remote NVMe tier for long-term session resume.",
        )
    return PlacementDecision(
        block_id=block.block_id,
        target_location=CacheLocation.EVICTED,
        score=importance,
        estimated_transfer_time_ms=0.0,
        reason="Utility negligible; evicting completely.",
    )
