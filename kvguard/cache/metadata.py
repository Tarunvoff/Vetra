"""Metadata extraction and tagging utilities."""

from typing import Any, Dict
from kvguard.core.models import KVBlockStats


class BlockMetadataHelper:
    """Helper for managing block-level tags and session metadata."""

    @staticmethod
    def enrich_metadata(block: KVBlockStats, tags: Dict[str, Any]) -> KVBlockStats:
        """Enrich existing block metadata with additional diagnostic tags."""
        new_block = block.model_copy()
        new_block.metadata.update(tags)
        return new_block

    @staticmethod
    def is_expired(block: KVBlockStats, now_timestamp_seconds: float) -> bool:
        """Check whether block TTL has elapsed."""
        if block.ttl_seconds is None:
            return False
        age = now_timestamp_seconds - block.created_at.timestamp()
        return age > block.ttl_seconds
