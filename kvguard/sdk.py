"""Public Python SDK for integrating KVGuard into inference applications."""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional
from kvguard.api.dependencies import ServiceContainer
from kvguard.config import Settings, load_settings
from kvguard.core.enums import EngineType, ExecutionMode
from kvguard.core.models import Recommendation
from kvguard.api.schemas.stats import StatsOverviewResponse


class KVGuard:
    """High-level Python client for controlling KVGuard."""

    def __init__(
        self,
        engine: str = "vllm",
        policy: str = "rule_based",
        mode: str = "simulation",
        vllm_url: str = "http://localhost:8000",
        redis_url: str = "redis://localhost:6379/0",
        config_path: Optional[str] = None,
    ) -> None:
        self.settings: Settings = load_settings(config_path)
        self.settings.engine = EngineType(engine.lower())
        self.settings.execution_mode = ExecutionMode(mode.lower())
        self.settings.vllm.base_url = vllm_url
        self.settings.redis.url = redis_url

        self._container = ServiceContainer(self.settings)
        self._loop = None
        self._is_running = False

    def start(self) -> None:
        """Synchronously start background telemetry and connections."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        self._loop = loop
        if not loop.is_running():
            loop.run_until_complete(self._container.initialize())
        else:
            asyncio.create_task(self._container.initialize())
        self._is_running = True

    async def astart(self) -> None:
        """Asynchronously start KVGuard services."""
        await self._container.initialize()
        self._is_running = True

    def stop(self) -> None:
        """Synchronously stop background telemetry."""
        if self._loop and not self._loop.is_running():
            self._loop.run_until_complete(self._container.shutdown())
        self._is_running = False

    async def astop(self) -> None:
        """Asynchronously stop KVGuard services."""
        await self._container.shutdown()
        self._is_running = False

    def stats(self) -> Dict[str, Any]:
        """Fetch real-time GPU and cache statistics."""
        async def _fetch():
            gpu = await self._container.engine_adapter.get_gpu_stats()
            cache = await self._container.engine_adapter.get_cache_stats()
            return {"gpu": gpu.model_dump(), "cache": cache}

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if not loop.is_running():
            return loop.run_until_complete(_fetch())
        else:
            future = asyncio.run_coroutine_threadsafe(_fetch(), loop)
            return future.result()

    def recommendations(self) -> List[Dict[str, Any]]:
        """Fetch current policy recommendations."""
        async def _fetch():
            gpu = await self._container.engine_adapter.get_gpu_stats()
            blocks = await self._container.metadata_repo.list_blocks(limit=100)
            if not blocks:
                blocks = await self._container.engine_adapter.get_block_stats()

            recs = [
                self._container.policy_engine.evaluate(b, gpu, b.importance_score).model_dump()
                for b in blocks
            ]
            return recs

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if not loop.is_running():
            return loop.run_until_complete(_fetch())
        else:
            future = asyncio.run_coroutine_threadsafe(_fetch(), loop)
            return future.result()
