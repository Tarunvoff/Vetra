"""Cache lifecycle state machine and transition validation."""

from __future__ import annotations

from typing import Set
from kvguard.core.enums import CacheLocation, DecisionType
from kvguard.core.models import KVBlockStats
from kvguard.exceptions import PolicyError

VALID_TRANSITIONS: dict[CacheLocation, Set[CacheLocation]] = {
    CacheLocation.GPU: {CacheLocation.CPU, CacheLocation.REMOTE, CacheLocation.EVICTED, CacheLocation.GPU},
    CacheLocation.CPU: {CacheLocation.GPU, CacheLocation.REMOTE, CacheLocation.EVICTED, CacheLocation.CPU},
    CacheLocation.REMOTE: {CacheLocation.GPU, CacheLocation.CPU, CacheLocation.EVICTED, CacheLocation.REMOTE},
    CacheLocation.EVICTED: {CacheLocation.GPU},  # Re-allocated upon cache miss
}


class CacheLifecycleManager:
    """Validates and applies logical cache state transitions."""

    @staticmethod
    def transition(block: KVBlockStats, target_location: CacheLocation) -> KVBlockStats:
        """Validate and update location of a block."""
        allowed = VALID_TRANSITIONS.get(block.location, set())
        if target_location not in allowed:
            raise PolicyError(
                f"Invalid location transition for block '{block.block_id}': {block.location} -> {target_location}"
            )

        updated = block.model_copy()
        updated.location = target_location

        if target_location == CacheLocation.GPU:
            updated.gpu_memory_bytes = block.gpu_memory_bytes or block.cpu_memory_bytes
            updated.cpu_memory_bytes = 0
        elif target_location == CacheLocation.CPU:
            updated.cpu_memory_bytes = block.gpu_memory_bytes or block.cpu_memory_bytes
            updated.gpu_memory_bytes = 0
        elif target_location == CacheLocation.EVICTED:
            updated.gpu_memory_bytes = 0
            updated.cpu_memory_bytes = 0

        return updated
