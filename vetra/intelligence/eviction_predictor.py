"""Predictive eviction risk scorer."""

from vetra.core.models import KVBlockStats


class EvictionPredictor:
    """Estimates optimal eviction sequence to minimize future recomputation."""

    @staticmethod
    def predict_eviction_urgency(block: KVBlockStats, current_gpu_pressure: float) -> float:
        """Score in [0.0, 1.0] where 1.0 indicates highest priority to evict."""
        inv_importance = 1.0 - block.importance_score
        pressure_factor = current_gpu_pressure
        return round((inv_importance * 0.7) + (pressure_factor * 0.3), 3)
