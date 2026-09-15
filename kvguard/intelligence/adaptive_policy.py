"""Adaptive policy coordinator choosing active strategy based on dynamic workload."""

from kvguard.core.models import GPUStats, KVBlockStats, Recommendation
from kvguard.intelligence.reuse_predictor import ReusePredictor
from kvguard.policy.engine import PolicyEngine


class AdaptivePolicy:
    """Dynamically adjusts policy parameters based on observed workload dynamics."""

    def __init__(self) -> None:
        self.predictor = ReusePredictor()
        self.engine = PolicyEngine()

    def decide(self, block: KVBlockStats, gpu_stats: GPUStats) -> Recommendation:
        pred = self.predictor.predict(block)
        # Blend static importance with dynamic reuse probability
        dynamic_importance = (block.importance_score * 0.5) + (pred.reuse_probability * 0.5)
        return self.engine.evaluate(block, gpu_stats, dynamic_importance)
