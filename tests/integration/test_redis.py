import pytest
from kvguard.cache.block import create_sample_block
from kvguard.storage.memory import InMemoryMetadataRepository
from kvguard.storage.redis import RedisMetadataRepository


@pytest.mark.asyncio
async def test_in_memory_metadata_repository():
    repo = InMemoryMetadataRepository()
    block = create_sample_block("blk_test_10", tenant_id="tenant_x")

    await repo.save_block(block)
    retrieved = await repo.get_block("blk_test_10")
    assert retrieved is not None
    assert retrieved.tenant_id == "tenant_x"

    await repo.record_hit("blk_test_10")
    retrieved = await repo.get_block("blk_test_10")
    assert retrieved.hit_count >= 1

    blocks = await repo.list_blocks(tenant_id="tenant_x")
    assert len(blocks) == 1

    deleted = await repo.delete_block("blk_test_10")
    assert deleted is True
    assert await repo.get_block("blk_test_10") is None


@pytest.mark.asyncio
async def test_redis_fallback_repository():
    # Attempting unreachable port with fallback enabled
    repo = RedisMetadataRepository(url="redis://localhost:9999/0", use_in_memory_fallback=True)
    await repo.initialize()

    block = create_sample_block("blk_fallback_01")
    await repo.save_block(block)
    retrieved = await repo.get_block("blk_fallback_01")
    assert retrieved is not None
    assert retrieved.block_id == "blk_fallback_01"
