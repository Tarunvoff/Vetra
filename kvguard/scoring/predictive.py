"""Machine learning importance scorer stub for Phase 3+."""

from typing import Any, Dict, Optional
from kvguard.core.interfaces import IImportanceScorer
from kvguard.core.models import KVBlockStats
from kvguard.scoring.importance import compute_importance


class MLImportanceScorer(IImportanceScorer):
    """Predictive ML Scorer stub (falls back to rule-based until model weights are loaded)."""

    def __init__(self, model_path: Optional[str] = None) -> None:
        self.model_path = model_path
        self._model_loaded = False

    def compute_importance(
        self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None
    ) -> float:
        # Falls back cleanly to explainable rule-based scoring until trained ML model is supplied
        return compute_importance(block)
