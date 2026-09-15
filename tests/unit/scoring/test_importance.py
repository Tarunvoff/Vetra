from vetra.core.models import KVBlockStats
from vetra.scoring.importance import compute_importance


def test_compute_importance_normalized(sample_block: KVBlockStats):
    score = compute_importance(
        sample_block, recency_weight=0.4, frequency_weight=0.3, reuse_weight=0.3
    )
    assert 0.0 <= score <= 1.0
