"""Recommendation formatting and reasoning builder."""

from vetra.core.enums import DecisionType
from vetra.core.models import KVBlockStats, Recommendation


def build_recommendation(
    block: KVBlockStats,
    decision: DecisionType,
    importance: float,
    reason: str,
    gpu_pressure: float = 0.0,
) -> Recommendation:
    """Construct a validated Recommendation object with expected memory savings."""
    mem_saving = 0
    latency_delta = 0.0

    if decision in (DecisionType.OFFLOAD_CPU, DecisionType.EVICT):
        mem_saving = block.gpu_memory_bytes
        latency_delta = 15.0 if decision == DecisionType.OFFLOAD_CPU else 80.0
    elif decision == DecisionType.PREFETCH:
        latency_delta = -20.0  # Prefetch improves TTFT

    confidence = 0.95 if gpu_pressure > 0.85 else 0.85

    return Recommendation(
        block_id=block.block_id,
        tenant_id=block.tenant_id,
        decision=decision,
        score=importance,
        reason=reason,
        expected_memory_saving_bytes=mem_saving,
        expected_latency_delta_ms=latency_delta,
        confidence=confidence,
    )
