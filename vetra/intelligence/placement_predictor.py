"""Predictive placement target selector."""

from vetra.core.enums import CacheLocation
from vetra.core.models import GPUStats, KVBlockStats, Prediction


class PlacementPredictor:
    """Combines predicted reuse and current pressure to select optimal tier."""

    @staticmethod
    def predict_optimal_tier(
        block: KVBlockStats, prediction: Prediction, gpu_stats: GPUStats
    ) -> CacheLocation:
        if gpu_stats.memory_pressure < 0.80 or prediction.reuse_probability >= 0.70:
            return CacheLocation.GPU
        elif prediction.reuse_probability >= 0.30:
            return CacheLocation.CPU
        return CacheLocation.EVICTED
