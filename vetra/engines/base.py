"""Base engine adapter implementing IInferenceEngineAdapter."""

from __future__ import annotations

from typing import Any, Dict, List
from vetra.core.interfaces import IInferenceEngineAdapter
from vetra.core.models import (
    EngineCapabilities,
    GPUStats,
    KVBlockStats,
    RequestStats,
    UnifiedDecision,
)


class BaseInferenceEngineAdapter(IInferenceEngineAdapter):
    """Base class providing default safe fallbacks for engine adapters."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._connected: bool = False

    async def connect(self) -> bool:
        self._connected = True
        return True

    async def disconnect(self) -> None:
        self._connected = False

    async def health(self) -> bool:
        return self._connected

    async def apply_decision(self, decision: UnifiedDecision) -> Dict[str, Any]:
        """Default safe implementation: recommendation only, no mutation."""
        return {
            "status": "recommendation_only",
            "block_id": decision.block_id,
            "decision": decision.decision.value,
            "applied": False,
            "reason": "Direct engine cache mutation not supported or dry-run enabled",
        }
