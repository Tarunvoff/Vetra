"""Simulation state objects modeling synthetic GPU, KV blocks, and cache transitions."""

from __future__ import annotations

import random
from typing import Dict, List, Optional
from vetra.cache.block import create_sample_block
from vetra.core.enums import CacheLocation, DecisionType
from vetra.core.models import GPUStats, KVBlockStats, RequestStats


class SimulatedGPU:
    """Simulates physical GPU memory consumption and pressure fluctuations."""

    def __init__(self, total_memory_gb: int = 80, base_utilization: float = 0.65) -> None:
        self.total_memory_bytes = total_memory_gb * 1024 * 1024 * 1024
        self.base_utilization = base_utilization
        self.current_pressure = base_utilization

    def set_pressure(self, pressure: float) -> None:
        self.current_pressure = max(0.0, min(1.0, pressure))

    def step(self, delta: float = 0.0) -> GPUStats:
        # Add slight natural jitter
        jitter = (random.random() - 0.5) * 0.04
        self.current_pressure = max(0.1, min(0.98, self.current_pressure + delta + jitter))

        used_bytes = int(self.total_memory_bytes * self.current_pressure)
        kv_bytes = int(used_bytes * 0.60)

        return GPUStats(
            total_memory_bytes=self.total_memory_bytes,
            used_memory_bytes=used_bytes,
            free_memory_bytes=max(0, self.total_memory_bytes - used_bytes),
            utilization_percent=round(self.current_pressure * 100.0, 1),
            kv_memory_bytes=kv_bytes,
            kv_utilization_percent=round(self.current_pressure * 80.0, 1),
            device_name="Simulated NVIDIA H100 80GB HBM3",
        )


class SimulatedKVCache:
    """Manages simulated active blocks, hit/miss ratios, and offload/eviction operations."""

    def __init__(self) -> None:
        self.blocks: Dict[str, KVBlockStats] = {}
        self._seed_initial_blocks()

    def _seed_initial_blocks(self, count: int = 25) -> None:
        for i in range(count):
            bid = f"sim_blk_{i:03d}"
            tenant = f"tenant_{i % 3}"
            session = f"session_{i % 5}"
            tokens = 16
            importance = round(random.uniform(0.15, 0.95), 2)
            blk = create_sample_block(
                block_id=bid,
                tenant_id=tenant,
                session_id=session,
                token_count=tokens,
                importance=importance,
            )
            blk.access_count = random.randint(1, 15)
            blk.reuse_count = random.randint(0, 6)
            blk.hit_count = random.randint(0, 8)
            self.blocks[bid] = blk

    def generate_random_block(self, tenant_id: str = "default") -> KVBlockStats:
        bid = f"sim_blk_{len(self.blocks):04d}"
        blk = create_sample_block(
            block_id=bid,
            tenant_id=tenant_id,
            session_id=f"session_{random.randint(1, 10)}",
            importance=round(random.uniform(0.1, 0.9), 2),
        )
        self.blocks[bid] = blk
        return blk
