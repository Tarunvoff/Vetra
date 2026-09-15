"""Rolling time-window telemetry aggregator."""

from __future__ import annotations

import asyncio
from collections import deque
from datetime import datetime, timezone
from typing import Deque, List, Optional
from vetra.core.models import GPUStats, RequestStats
from vetra.telemetry.schemas import AggregatedMetrics, TelemetrySnapshot


class TelemetryAggregator:
    """Aggregates point-in-time telemetry snapshots over sliding time windows."""

    def __init__(self, window_seconds: float = 60.0) -> None:
        self.window_seconds = window_seconds
        self._snapshots: Deque[TelemetrySnapshot] = deque(maxlen=300)
        self._lock = asyncio.Lock()

    async def add_snapshot(self, snapshot: TelemetrySnapshot) -> None:
        async with self._lock:
            self._snapshots.append(snapshot)

    async def get_latest_snapshot(self) -> Optional[TelemetrySnapshot]:
        async with self._lock:
            return self._snapshots[-1] if self._snapshots else None

    async def get_aggregated_metrics(self) -> AggregatedMetrics:
        async with self._lock:
            if not self._snapshots:
                return AggregatedMetrics()

            now = datetime.now(timezone.utc)
            valid_snapshots = [
                s for s in self._snapshots
                if (now - s.timestamp).total_seconds() <= self.window_seconds
            ]

            if not valid_snapshots:
                valid_snapshots = list(self._snapshots)[-10:]

            count = len(valid_snapshots)
            avg_util = sum(s.gpu_stats.utilization_percent for s in valid_snapshots) / count
            avg_kv_mem = sum(s.gpu_stats.kv_memory_bytes for s in valid_snapshots) / count
            avg_hit = sum(s.cache_hit_rate for s in valid_snapshots) / count

            return AggregatedMetrics(
                window_seconds=self.window_seconds,
                sample_count=count,
                avg_gpu_utilization=avg_util,
                avg_kv_memory_bytes=avg_kv_mem,
                avg_hit_rate=avg_hit,
            )
