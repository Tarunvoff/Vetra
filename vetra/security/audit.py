"""Security audit logger and trail recorder."""

from collections import deque
from typing import Deque, List
from vetra.core.models import AuditEvent, SecurityEvent


class SecurityAuditLogger:
    """Stores recent security authorization decisions and policy enforcement logs."""

    def __init__(self, max_records: int = 1000) -> None:
        self._events: Deque[SecurityEvent | AuditEvent] = deque(maxlen=max_records)

    def record_event(self, event: SecurityEvent | AuditEvent) -> None:
        self._events.append(event)

    def list_events(self, limit: int = 50) -> List[SecurityEvent | AuditEvent]:
        return list(self._events)[-limit:]
