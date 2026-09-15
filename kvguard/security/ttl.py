"""Time-to-Live (TTL) expiration validator."""

from datetime import datetime, timezone
from kvguard.core.models import KVBlockStats


class TTLManager:
    """Enforces expiration deadlines on tenant cache blocks."""

    @staticmethod
    def is_block_valid(block: KVBlockStats) -> bool:
        if block.ttl_seconds is None:
            return True
        now = datetime.now(timezone.utc)
        elapsed = (now - block.created_at).total_seconds()
        return elapsed <= block.ttl_seconds
