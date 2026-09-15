from vetra.core.enums import DecisionType
from vetra.core.models import GPUStats, KVBlockStats
from vetra.policy.engine import PolicyEngine


def test_policy_low_pressure_keep(sample_block: KVBlockStats, normal_gpu_stats: GPUStats):
    engine = PolicyEngine()
    rec = engine.evaluate(sample_block, normal_gpu_stats, importance_score=0.3)
    assert rec.decision == DecisionType.KEEP


def test_policy_high_pressure_evict(sample_block: KVBlockStats, high_pressure_gpu_stats: GPUStats):
    engine = PolicyEngine()
    rec = engine.evaluate(sample_block, high_pressure_gpu_stats, importance_score=0.15)
    assert rec.decision == DecisionType.EVICT
    assert "evicting" in rec.reason.lower()


def test_policy_high_pressure_offload(sample_block: KVBlockStats, high_pressure_gpu_stats: GPUStats):
    engine = PolicyEngine()
    rec = engine.evaluate(sample_block, high_pressure_gpu_stats, importance_score=0.55)
    assert rec.decision == DecisionType.OFFLOAD_CPU
