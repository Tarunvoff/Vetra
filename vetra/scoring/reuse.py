"""Reuse score calculation based on cross-request hits and reuses."""

from vetra.core.models import KVBlockStats


def calculate_reuse_score(block: KVBlockStats) -> float:
    """Calculate normalized reuse score in [0.0, 1.0].

    Considers cross-request reuse occurrences and hit rates:
    Score = (reuse_count * 2.0 + hit_count) / (access_count + 1)
    """
    total_reused = block.reuse_count * 2.0 + block.hit_count
    denominator = max(1, block.access_count + 1)
    score = total_reused / denominator
    return max(0.0, min(1.0, score))
