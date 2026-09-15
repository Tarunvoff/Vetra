from vetra.core.models import KVBlockStats
from vetra.scoring.frequency import calculate_frequency


def test_frequency_zero_access(sample_block: KVBlockStats):
    sample_block.access_count = 0
    score = calculate_frequency(sample_block)
    assert score == 0.0


def test_frequency_scaling(sample_block: KVBlockStats):
    sample_block.access_count = 10
    score_10 = calculate_frequency(sample_block, saturation_access_count=100)
    sample_block.access_count = 100
    score_100 = calculate_frequency(sample_block, saturation_access_count=100)

    assert 0.0 < score_10 < score_100 <= 1.0
