"""Event types and in-memory event publisher for KVGuard telemetry and lifecycle."""

from __future__ import annotations

import asyncio
from typing import Callable, Coroutine, Dict, List, Any
from kvguard.core.models import CacheEvent, SecurityEvent, AuditEvent


EventHandler = Callable[[Any], Coroutine[Any, Any, None]]


class EventBus:
    """Lightweight async event bus for internal telemetry and audit events."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[EventHandler]] = {}

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe an async handler to a specific event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    async def publish(self, event_type: str, event_data: Any) -> None:
        """Publish an event to all registered subscribers."""
        handlers = self._subscribers.get(event_type, [])
        if handlers:
            tasks = [asyncio.create_task(handler(event_data)) for handler in handlers]
            await asyncio.gather(*tasks, return_exceptions=True)


# Global event bus singleton
global_event_bus = EventBus()
