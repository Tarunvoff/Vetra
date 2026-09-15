"""Redis metadata repository for production cache metadata storage with in-memory fallback."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import List, Optional
import redis.asyncio as aioredis
from kvguard.core.interfaces import ICacheMetadataRepository
from kvguard.core.models import KVBlockStats
from kvguard.exceptions import StorageError
from kvguard.storage.memory import InMemoryMetadataRepository


class RedisMetadataRepository(ICacheMetadataRepository):
    """Production Redis metadata repository storing JSON-serialized block models."""

    def __init__(
        self,
        url: str = "redis://localhost:6379/0",
        key_prefix: str = "kvguard:",
        use_in_memory_fallback: bool = True,
        connection_timeout: float = 2.0,
    ) -> None:
        self.url = url
        self.key_prefix = key_prefix
        self.use_in_memory_fallback = use_in_memory_fallback
        self.connection_timeout = connection_timeout
        self._redis: Optional[aioredis.Redis] = None
        self._fallback = InMemoryMetadataRepository()
        self._is_redis_available = False

    def _block_key(self, block_id: str) -> str:
        return f"{self.key_prefix}block:{block_id}"

    def _index_key(self, tenant_id: str = "default") -> str:
        return f"{self.key_prefix}tenant_blocks:{tenant_id}"

    async def initialize(self) -> bool:
        """Test and establish Redis connection."""
        try:
            self._redis = aioredis.from_url(
                self.url,
                decode_responses=True,
                socket_connect_timeout=self.connection_timeout,
            )
            await self._redis.ping()
            self._is_redis_available = True
            return True
        except Exception:
            self._is_redis_available = False
            if not self.use_in_memory_fallback:
                raise StorageError(f"Could not connect to Redis at {self.url} and fallback is disabled.")
            return False

    async def save_block(self, block: KVBlockStats) -> None:
        if not self._is_redis_available or self._redis is None:
            await self._fallback.save_block(block)
            return

        try:
            data = block.model_dump_json()
            key = self._block_key(block.block_id)
            await self._redis.set(key, data)
            await self._redis.sadd(self._index_key(block.tenant_id), block.block_id)
            if block.ttl_seconds:
                await self._redis.expire(key, block.ttl_seconds)
        except Exception:
            await self._fallback.save_block(block)

    async def get_block(self, block_id: str) -> Optional[KVBlockStats]:
        if not self._is_redis_available or self._redis is None:
            return await self._fallback.get_block(block_id)

        try:
            data = await self._redis.get(self._block_key(block_id))
            if not data:
                return None
            return KVBlockStats.model_validate_json(data)
        except Exception:
            return await self._fallback.get_block(block_id)

    async def update_block(self, block: KVBlockStats) -> None:
        await self.save_block(block)

    async def delete_block(self, block_id: str) -> bool:
        if not self._is_redis_available or self._redis is None:
            return await self._fallback.delete_block(block_id)

        try:
            block = await self.get_block(block_id)
            if block:
                await self._redis.srem(self._index_key(block.tenant_id), block_id)
            res = await self._redis.delete(self._block_key(block_id))
            return res > 0
        except Exception:
            return await self._fallback.delete_block(block_id)

    async def list_blocks(
        self, tenant_id: Optional[str] = None, limit: int = 100, offset: int = 0
    ) -> List[KVBlockStats]:
        if not self._is_redis_available or self._redis is None:
            return await self._fallback.list_blocks(tenant_id, limit, offset)

        try:
            tenant = tenant_id or "default"
            block_ids = list(await self._redis.smembers(self._index_key(tenant)))
            sliced_ids = block_ids[offset : offset + limit]
            if not sliced_ids:
                return []

            keys = [self._block_key(bid) for bid in sliced_ids]
            raw_blocks = await self._redis.mget(keys)
            blocks: List[KVBlockStats] = []
            for item in raw_blocks:
                if item:
                    blocks.append(KVBlockStats.model_validate_json(item))
            return blocks
        except Exception:
            return await self._fallback.list_blocks(tenant_id, limit, offset)

    async def record_access(self, block_id: str, request_id: Optional[str] = None) -> None:
        block = await self.get_block(block_id)
        if block:
            block.access_count += 1
            block.last_accessed_at = datetime.now(timezone.utc)
            if request_id:
                block.request_id = request_id
            await self.save_block(block)

    async def record_reuse(self, block_id: str) -> None:
        block = await self.get_block(block_id)
        if block:
            block.reuse_count += 1
            block.access_count += 1
            block.last_accessed_at = datetime.now(timezone.utc)
            await self.save_block(block)

    async def record_hit(self, block_id: str) -> None:
        block = await self.get_block(block_id)
        if block:
            block.hit_count += 1
            block.access_count += 1
            block.last_accessed_at = datetime.now(timezone.utc)
            await self.save_block(block)

    async def record_miss(self, block_id: str) -> None:
        block = await self.get_block(block_id)
        if block:
            block.miss_count += 1
            block.last_accessed_at = datetime.now(timezone.utc)
            await self.save_block(block)

    async def clear(self) -> None:
        if self._is_redis_available and self._redis is not None:
            try:
                keys = await self._redis.keys(f"{self.key_prefix}*")
                if keys:
                    await self._redis.delete(*keys)
            except Exception:
                pass
        await self._fallback.clear()
