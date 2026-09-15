"""In-memory rolling buffer tracking recent requests and inference performance."""

from __future__ import annotations

import asyncio
from collections import deque
from typing import Deque, List
from kvguard.core.models import RequestStats


class RequestTracker:
    """Thread-safe sliding window of recent request statistics."""

    def __init__(self, max_size: int = 1000) -> None:
        self.max_size = max_size
        self._requests: Deque[RequestStats] = deque(maxlen=max_size)
        self._lock = asyncio.Lock()

    async def record_request(self, request: RequestStats) -> None:
        async with self._lock:
            self._requests.append(request)

    async def get_recent_requests(self, limit: int = 50) -> List[RequestStats]:
        async with self._lock:
            return list(self._requests)[-limit:]

    async def get_summary_stats(self) -> dict:
        async with self._lock:
            if not self._requests:
                return {
                    "total_requests": 0,
                    "avg_hit_rate": 0.0,
                    "avg_ttft_ms": 0.0,
                    "avg_latency_ms": 0.0,
                }

            reqs = list(self._requests)
            total = len(reqs)
            hit_count = sum(1 for r in reqs if r.cache_hit)
            ttfts = [r.ttft_ms for r in reqs if r.ttft_ms is not None]
            latencies = [r.total_latency_ms for r in reqs if r.total_latency_ms is not None]

            return {
                "total_requests": total,
                "avg_hit_rate": hit_count / total if total > 0 else 0.0,
                "avg_ttft_ms": sum(ttfts) / len(ttfts) if ttfts else 0.0,
                "avg_latency_ms": sum(latencies) / len(latencies) if latencies else 0.0,
            }
