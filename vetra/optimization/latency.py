"""Latency and TTFT impact estimators."""

from typing import Dict


class LatencyOptimizer:
    """Models cache hit speedup on Time to First Token (TTFT)."""

    @staticmethod
    def estimate_ttft_improvement(
        cached_tokens: int, tokens_per_second_compute: float = 2500.0
    ) -> Dict[str, float]:
        saved_compute_seconds = cached_tokens / max(1.0, tokens_per_second_compute)
        return {
            "cached_tokens": float(cached_tokens),
            "estimated_ttft_saved_ms": saved_compute_seconds * 1000.0,
        }
