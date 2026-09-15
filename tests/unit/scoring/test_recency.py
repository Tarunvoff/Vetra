from datetime import datetime, timedelta, timezone
from kvguard.core.models import KVBlockStats
from kvguard.scoring.recency import calculate_recency


def test_recency_fresh_block(sample_block: KVBlockStats):
    now = datetime.now(timezone.utc)
    sample_block.last_accessed_at = now
    score = calculate_recency(sample_block, current_time=now, half_life_seconds=300.0)
    assert 0.99 <= score <= 1.0


def test_recency_decay(sample_block: KVBlockStats):
    now = datetime.now(timezone.utc)
    sample_block.last_accessed_at = now - timedelta(seconds=300)
    score = calculate_recency(sample_block, current_time=now, half_life_seconds=300.0)
    assert abs(score - 0.5) < 0.05
