from vetra.core.models import KVBlockStats
from vetra.scoring.reuse import calculate_reuse_score


def test_reuse_score(sample_block: KVBlockStats):
    sample_block.access_count = 10
    sample_block.reuse_count = 3
    sample_block.hit_count = 2
    score = calculate_reuse_score(sample_block)
    assert 0.0 <= score <= 1.0
