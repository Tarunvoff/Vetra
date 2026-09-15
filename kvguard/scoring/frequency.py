"""Frequency scoring function with logarithmic scaling."""

import math
from kvguard.core.models import KVBlockStats


def calculate_frequency(block: KVBlockStats, saturation_access_count: int = 100) -> float:
    """Calculate normalized frequency score in [0.0, 1.0].

    Uses logarithmic scaling: Score = log(1 + access_count) / log(1 + saturation_count)
    This prevents high-frequency outliers from dominating policy calculations.
    """
    if block.access_count <= 0:
        return 0.0

    numerator = math.log1p(block.access_count)
    denominator = math.log1p(max(1, saturation_access_count))
    score = numerator / denominator
    return max(0.0, min(1.0, score))
