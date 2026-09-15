"""Pytest configuration and shared fixtures for Vetra tests."""

import pytest
from vetra.cache.block import create_sample_block
from vetra.core.models import GPUStats, KVBlockStats
from vetra.storage.memory import InMemoryMetadataRepository


@pytest.fixture
def sample_block() -> KVBlockStats:
    return create_sample_block(
        block_id="test_blk_001",
        tenant_id="tenant_a",
        session_id="session_100",
        token_count=16,
        importance=0.65,
    )


@pytest.fixture
def normal_gpu_stats() -> GPUStats:
    total = 80 * 1024 * 1024 * 1024
    used = int(total * 0.60)
    return GPUStats(
        total_memory_bytes=total,
        used_memory_bytes=used,
        free_memory_bytes=total - used,
        utilization_percent=60.0,
        kv_memory_bytes=int(used * 0.5),
        device_name="Test GPU",
    )


@pytest.fixture
def high_pressure_gpu_stats() -> GPUStats:
    total = 80 * 1024 * 1024 * 1024
    used = int(total * 0.94)
    return GPUStats(
        total_memory_bytes=total,
        used_memory_bytes=used,
        free_memory_bytes=total - used,
        utilization_percent=94.0,
        kv_memory_bytes=int(used * 0.7),
        device_name="Test GPU",
    )


@pytest.fixture
def memory_repo() -> InMemoryMetadataRepository:
    return InMemoryMetadataRepository()
