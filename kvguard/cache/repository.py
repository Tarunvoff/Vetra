"""Repository alias and factory helpers."""

from kvguard.core.interfaces import ICacheMetadataRepository
from kvguard.storage.memory import InMemoryMetadataRepository
from kvguard.storage.redis import RedisMetadataRepository


def create_metadata_repository(
    redis_url: str = "redis://localhost:6379/0",
    use_fallback: bool = True,
    key_prefix: str = "kvguard:",
) -> ICacheMetadataRepository:
    """Factory helper creating the appropriate metadata repository."""
    if use_fallback:
        return RedisMetadataRepository(
            url=redis_url,
            key_prefix=key_prefix,
            use_in_memory_fallback=True,
        )
    return InMemoryMetadataRepository()
