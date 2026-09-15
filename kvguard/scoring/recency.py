"""Recency scoring function with exponential decay."""

import math
from datetime import datetime, timezone
from kvguard.core.models import KVBlockStats


def calculate_recency(
    block: KVBlockStats,
    current_time: datetime | None = None,
    half_life_seconds: float = 300.0,
) -> float:
    """Calculate normalized recency score in [0.0, 1.0].

    Uses exponential decay: Score = 2^(-delta_t / half_life)
    Where delta_t is the time elapsed since last block access.
    """
    now = current_time or datetime.now(timezone.utc)
    delta_t = max(0.0, (now - block.last_accessed_at).total_seconds())

    if half_life_seconds <= 0:
        return 1.0 if delta_t == 0 else 0.0

    score = math.pow(2.0, -delta_t / half_life_seconds)
    return max(0.0, min(1.0, score))
