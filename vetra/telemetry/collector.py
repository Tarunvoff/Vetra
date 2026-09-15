"""Telemetry background polling collector."""

from __future__ import annotations

import asyncio
import logging
from typing import Optional
from vetra.core.interfaces import ICacheMetadataRepository, IInferenceEngineAdapter
from vetra.telemetry.aggregator import TelemetryAggregator
from vetra.telemetry.metrics import (
    CACHE_HIT_RATE,
    CACHE_MISS_RATE,
    GPU_MEMORY_BYTES,
    KV_MEMORY_BYTES,
)
from vetra.telemetry.request_tracker import RequestTracker
from vetra.telemetry.schemas import TelemetrySnapshot

logger = logging.getLogger("vetra.telemetry.collector")


class TelemetryCollector:
    """Polls inference engine adapter at configured intervals to ingest metrics."""

    def __init__(
        self,
        engine_adapter: IInferenceEngineAdapter,
        metadata_repo: ICacheMetadataRepository,
        aggregator: TelemetryAggregator,
        request_tracker: RequestTracker,
        interval_seconds: float = 2.0,
    ) -> None:
        self.adapter = engine_adapter
        self.repo = metadata_repo
        self.aggregator = aggregator
        self.request_tracker = request_tracker
        self.interval = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        """Start the async polling loop."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._poll_loop())
        logger.info(f"Telemetry collector started with {self.interval}s interval.")

    async def stop(self) -> None:
        """Stop the background polling loop."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None
        logger.info("Telemetry collector stopped.")

    async def poll_once(self) -> TelemetrySnapshot:
        """Execute a single telemetry poll step."""
        gpu_stats = await self.adapter.get_gpu_stats()
        cache_stats = await self.adapter.get_cache_stats()
        recent_reqs = await self.adapter.get_request_stats()

        for req in recent_reqs:
            await self.request_tracker.record_request(req)

        hit_rate = cache_stats.get("cache_hit_rate", 0.0)
        miss_rate = max(0.0, 1.0 - hit_rate)

        # Update Prometheus Gauges
        GPU_MEMORY_BYTES.set(gpu_stats.used_memory_bytes)
        KV_MEMORY_BYTES.set(gpu_stats.kv_memory_bytes)
        CACHE_HIT_RATE.set(hit_rate)
        CACHE_MISS_RATE.set(miss_rate)

        # Count tracked blocks
        blocks = await self.repo.list_blocks(limit=1000)

        snapshot = TelemetrySnapshot(
            gpu_stats=gpu_stats,
            cache_stats=cache_stats,
            active_requests=int(cache_stats.get("num_requests_running", 0)),
            total_blocks_tracked=len(blocks),
            cache_hit_rate=hit_rate,
            cache_miss_rate=miss_rate,
            recent_requests=recent_reqs,
        )

        await self.aggregator.add_snapshot(snapshot)
        return snapshot

    async def _poll_loop(self) -> None:
        while self._running:
            try:
                await self.poll_once()
            except Exception as e:
                logger.debug(f"Telemetry collection tick exception: {e}")
            await asyncio.sleep(self.interval)
