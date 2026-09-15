from vetra.cache.lifecycle import CacheLifecycleManager
from vetra.core.enums import CacheLocation
from vetra.core.models import KVBlockStats


def test_lifecycle_transition_to_cpu(sample_block: KVBlockStats):
    sample_block.gpu_memory_bytes = 1048576
    updated = CacheLifecycleManager.transition(sample_block, CacheLocation.CPU)
    assert updated.location == CacheLocation.CPU
    assert updated.cpu_memory_bytes == 1048576
    assert updated.gpu_memory_bytes == 0
