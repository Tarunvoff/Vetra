"""Thread-safe in-memory cache metadata repository for simulation and testing."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Dict, List, Optional
from vetra.core.interfaces import ICacheMetadataRepository
from vetra.core.models import KVBlockStats


class InMemoryMetadataRepository(ICacheMetadataRepository):
    """In-memory metadata repository using asyncio Lock."""

    def __init__(self) -> None:
        self._blocks: Dict[str, KVBlockStats] = {}
        self._lock = asyncio.Lock()

    async def save_block(self, block: KVBlockStats) -> None:
        async with self._lock:
            self._blocks[block.block_id] = block.model_copy()

    async def get_block(self, block_id: str) -> Optional[KVBlockStats]:
        async with self._lock:
            block = self._blocks.get(block_id)
            return block.model_copy() if block else None

    async def update_block(self, block: KVBlockStats) -> None:
        async with self._lock:
            self._blocks[block.block_id] = block.model_copy()

    async def delete_block(self, block_id: str) -> bool:
        async with self._lock:
            return self._blocks.pop(block_id, None) is not None

    async def list_blocks(
        self, tenant_id: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[KVBlockStats]:
        async with self._lock:
            all_blocks = list(self._blocks.values())
            if tenant_id:
                all_blocks = [b for b in all_blocks if b.tenant_id == tenant_id]

            # Sort by last accessed descending
            all_blocks.sort(key=lambda b: b.last_accessed_at, reverse=True)
            sliced = all_blocks[offset : offset + limit]
            return [b.model_copy() for b in sliced]

    async def record_access(self, block_id: str, request_id: Optional[str] = None) -> None:
        async with self._lock:
            if block_id in self._blocks:
                block = self._blocks[block_id]
                block.access_count += 1
                block.last_accessed_at = datetime.now(timezone.utc)
                if request_id:
                    block.request_id = request_id

    async def record_reuse(self, block_id: str) -> None:
        async with self._lock:
            if block_id in self._blocks:
                block = self._blocks[block_id]
                block.reuse_count += 1
                block.access_count += 1
                block.last_accessed_at = datetime.now(timezone.utc)

    async def record_hit(self, block_id: str) -> None:
        async with self._lock:
            if block_id in self._blocks:
                block = self._blocks[block_id]
                block.hit_count += 1
                block.access_count += 1
                block.last_accessed_at = datetime.now(timezone.utc)

    async def record_miss(self, block_id: str) -> None:
        async with self._lock:
            if block_id in self._blocks:
                block = self._blocks[block_id]
                block.miss_count += 1
                block.last_accessed_at = datetime.now(timezone.utc)

    async def clear(self) -> None:
        async with self._lock:
            self._blocks.clear()

    async def count(self) -> int:
        async with self._lock:
            return len(self._blocks)
