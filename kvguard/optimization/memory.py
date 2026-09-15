"""Memory budget optimization and watermark enforcement."""

from typing import List
from kvguard.core.models import GPUStats, KVBlockStats


class MemoryBudgetOptimizer:
    """Computes memory targets to maintain GPU headroom."""

    @staticmethod
    def calculate_eviction_target_bytes(
        gpu_stats: GPUStats, target_utilization: float = 0.80
    ) -> int:
        target_bytes = int(gpu_stats.total_memory_bytes * target_utilization)
        if gpu_stats.used_memory_bytes <= target_bytes:
            return 0
        return gpu_stats.used_memory_bytes - target_bytes

    @staticmethod
    def select_eviction_candidates(
        blocks: List[KVBlockStats], required_bytes: int
    ) -> List[KVBlockStats]:
        sorted_blocks = sorted(blocks, key=lambda b: b.importance_score)
        selected: List[KVBlockStats] = []
        freed = 0
        for b in sorted_blocks:
            if freed >= required_bytes:
                break
            selected.append(b)
            freed += b.gpu_memory_bytes or 131072
        return selected
