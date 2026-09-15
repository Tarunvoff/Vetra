"""Predictive reuse forecast engine (Heuristic Phase 1 / ML interface Phase 3)."""

from typing import Any, Dict, Optional
from kvguard.core.interfaces import IReusePredictor
from kvguard.core.models import KVBlockStats, Prediction
from kvguard.scoring.reuse import calculate_reuse_score


class ReusePredictor(IReusePredictor):
    """Predicts KV block reuse probability over future time horizons.

    NOTE: Currently operates in HEURISTIC MODE based on access frequency and recent hits.
    Interfaces remain fixed for Phase 3 ML replacement (gradient boosting / neural sequence model).
    """

    def predict(self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None) -> Prediction:
        # Heuristic combination of reuse frequency and session indicators
        base_reuse = calculate_reuse_score(block)
        session_bonus = 0.2 if block.session_id else 0.0

        raw_prob = (base_reuse * 0.7) + session_bonus
        prob = max(0.05, min(0.95, raw_prob))

        confidence = 0.90 if block.access_count > 5 else 0.65

        return Prediction(
            reuse_probability=round(prob, 3),
            confidence=round(confidence, 2),
            horizon_seconds=120.0,
            model_type="heuristic_v1",
            features_used=["access_count", "reuse_count", "hit_count", "session_id"],
        )
