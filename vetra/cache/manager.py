"""High-level Cache Manager coordinating repository, lifecycle, and access tracking."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List, Optional
from vetra.cache.block import calculate_kv_block_bytes
from vetra.cache.lifecycle import CacheLifecycleManager
from vetra.core.enums import CacheLocation
from vetra.core.interfaces import ICacheMetadataRepository
from vetra.core.models import KVBlockStats


class CacheManager:
    """Manages logical KV block lifecycle and repository operations."""

    def __init__(self, repository: ICacheMetadataRepository) -> None:
        self.repo = repository

    async def register_block(
        self,
        block_id: str,
        tenant_id: str = "default",
        session_id: Optional[str] = None,
        request_id: Optional[str] = None,
        token_count: int = 16,
        location: CacheLocation = CacheLocation.GPU,
        ttl_seconds: Optional[int] = None,
    ) -> KVBlockStats:
        """Register a new KV cache block in the metadata store."""
        mem_bytes = calculate_kv_block_bytes(token_count=token_count)
        gpu_bytes = mem_bytes if location == CacheLocation.GPU else 0
        cpu_bytes = mem_bytes if location == CacheLocation.CPU else 0

        block = KVBlockStats(
            block_id=block_id,
            tenant_id=tenant_id,
            session_id=session_id,
            request_id=request_id,
            token_count=token_count,
            gpu_memory_bytes=gpu_bytes,
            cpu_memory_bytes=cpu_bytes,
            location=location,
            importance_score=0.5,
            ttl_seconds=ttl_seconds,
        )
        await self.repo.save_block(block)
        return block

    async def get_block(self, block_id: str) -> Optional[KVBlockStats]:
        return await self.repo.get_block(block_id)

    async def list_blocks(
        self, tenant_id: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[KVBlockStats]:
        return await self.repo.list_blocks(tenant_id=tenant_id, limit=limit, offset=offset)

    async def update_location(self, block_id: str, target_location: CacheLocation) -> Optional[KVBlockStats]:
        block = await self.repo.get_block(block_id)
        if not block:
            return None

        updated = CacheLifecycleManager.transition(block, target_location)
        await self.repo.update_block(updated)
        return updated
