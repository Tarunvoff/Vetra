"""Explainable importance scoring combining recency, frequency, and reuse."""

from __future__ import annotations

from typing import Any, Dict, Optional
from kvguard.core.interfaces import IImportanceScorer
from kvguard.core.models import KVBlockStats
from kvguard.scoring.frequency import calculate_frequency
from kvguard.scoring.recency import calculate_recency
from kvguard.scoring.reuse import calculate_reuse_score


def compute_importance(
    block: KVBlockStats,
    recency_weight: float = 0.4,
    frequency_weight: float = 0.3,
    reuse_weight: float = 0.3,
    half_life_seconds: float = 300.0,
) -> float:
    """Calculate normalized, explainable importance score [0.0, 1.0].

    Formula:
        importance = (w_r * recency) + (w_f * frequency) + (w_u * reuse)
    Weights are normalized if their sum does not equal 1.0.
    """
    total_w = recency_weight + frequency_weight + reuse_weight
    if total_w <= 0:
        total_w = 1.0
        recency_weight = frequency_weight = reuse_weight = 1.0 / 3.0

    w_r = recency_weight / total_w
    w_f = frequency_weight / total_w
    w_u = reuse_weight / total_w

    r_score = calculate_recency(block, half_life_seconds=half_life_seconds)
    f_score = calculate_frequency(block)
    u_score = calculate_reuse_score(block)

    importance = (w_r * r_score) + (w_f * f_score) + (w_u * u_score)
    return max(0.0, min(1.0, importance))


class RuleBasedScorer(IImportanceScorer):
    """Production explainable importance scorer for Phase 1."""

    def __init__(
        self,
        recency_weight: float = 0.4,
        frequency_weight: float = 0.3,
        reuse_weight: float = 0.3,
        half_life_seconds: float = 300.0,
    ) -> None:
        self.recency_weight = recency_weight
        self.frequency_weight = frequency_weight
        self.reuse_weight = reuse_weight
        self.half_life_seconds = half_life_seconds

    def compute_importance(
        self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None
    ) -> float:
        return compute_importance(
            block=block,
            recency_weight=self.recency_weight,
            frequency_weight=self.frequency_weight,
            reuse_weight=self.reuse_weight,
            half_life_seconds=self.half_life_seconds,
        )
