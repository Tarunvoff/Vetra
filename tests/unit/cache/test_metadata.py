from datetime import datetime, timezone
from kvguard.cache.metadata import BlockMetadataHelper
from kvguard.core.models import KVBlockStats


def test_metadata_ttl_expiry(sample_block: KVBlockStats):
    sample_block.ttl_seconds = 60
    now = sample_block.created_at.timestamp() + 100
    expired = BlockMetadataHelper.is_expired(sample_block, now)
    assert expired is True
