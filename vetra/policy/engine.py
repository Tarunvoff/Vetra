"""Production rule-based policy engine generating explainable recommendations."""

from __future__ import annotations

from typing import Any, Dict, Optional
from vetra.core.enums import CacheLocation, DecisionType
from vetra.core.interfaces import IPolicyEngine
from vetra.core.models import GPUStats, KVBlockStats, PolicyConstraints, Recommendation
from vetra.policy.recommendation import build_recommendation


class PolicyEngine(IPolicyEngine):
    """Rule-based decision engine balancing GPU memory pressure and block importance."""

    def __init__(
        self,
        gpu_pressure_high: float = 0.90,
        gpu_pressure_medium: float = 0.75,
        min_importance_to_keep: float = 0.60,
        min_importance_to_offload: float = 0.25,
    ) -> None:
        self.gpu_pressure_high = gpu_pressure_high
        self.gpu_pressure_medium = gpu_pressure_medium
        self.min_importance_to_keep = min_importance_to_keep
        self.min_importance_to_offload = min_importance_to_offload

    def evaluate(
        self,
        block: KVBlockStats,
        gpu_stats: GPUStats,
        importance_score: float,
        constraints: Optional[PolicyConstraints] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> Recommendation:
        pressure = gpu_stats.memory_pressure
        location = block.location

        # Check if block on CPU should be prefetched
        if location == CacheLocation.CPU:
            if importance_score >= 0.70 and pressure < self.gpu_pressure_medium:
                reason = (
                    f"GPU pressure is low ({pressure:.1%}) and CPU block has high importance ({importance_score:.2f}); "
                    "recommend prefetching to GPU."
                )
                return build_recommendation(block, DecisionType.PREFETCH, importance_score, reason, pressure)
            else:
                reason = (
                    f"Block is residing on CPU with importance {importance_score:.2f}; keeping in CPU memory."
                )
                return build_recommendation(block, DecisionType.NO_OP, importance_score, reason, pressure)

        # 1. Low GPU Pressure (< medium threshold)
        if pressure < self.gpu_pressure_medium:
            reason = (
                f"GPU pressure is low ({pressure:.1%}); keeping block {block.block_id} in GPU cache "
                f"(importance: {importance_score:.2f})."
            )
            return build_recommendation(block, DecisionType.KEEP, importance_score, reason, pressure)

        # 2. Medium GPU Pressure (medium <= pressure < high)
        elif pressure < self.gpu_pressure_high:
            if importance_score >= self.min_importance_to_keep:
                reason = (
                    f"GPU pressure is moderate ({pressure:.1%}); retaining high-importance block "
                    f"({importance_score:.2f} >= {self.min_importance_to_keep:.2f}) on GPU."
                )
                return build_recommendation(block, DecisionType.KEEP, importance_score, reason, pressure)
            else:
                reason = (
                    f"GPU pressure is moderate ({pressure:.1%}) and block importance is {importance_score:.2f}; "
                    f"offloading to CPU to preserve headroom."
                )
                return build_recommendation(block, DecisionType.OFFLOAD_CPU, importance_score, reason, pressure)

        # 3. High GPU Pressure (>= high threshold)
        else:
            if importance_score >= 0.80:
                reason = (
                    f"GPU pressure is critical ({pressure:.1%}); retaining top-tier block "
                    f"({importance_score:.2f}) on GPU."
                )
                return build_recommendation(block, DecisionType.KEEP, importance_score, reason, pressure)
            elif importance_score >= self.min_importance_to_offload:
                reason = (
                    f"GPU pressure is critical ({pressure:.1%}) and block importance is {importance_score:.2f}; "
                    "offloading block to CPU."
                )
                return build_recommendation(block, DecisionType.OFFLOAD_CPU, importance_score, reason, pressure)
            else:
                reason = (
                    f"GPU pressure is critical ({pressure:.1%}) and block importance is {importance_score:.2f} "
                    f"(< {self.min_importance_to_offload:.2f}); evicting low-utility block."
                )
                return build_recommendation(block, DecisionType.EVICT, importance_score, reason, pressure)
