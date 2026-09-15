"""Asynchronous collector querying vLLM HTTP endpoints."""

from __future__ import annotations

import httpx
from typing import Dict, Optional
from kvguard.exceptions import EngineConnectionError, EngineMetricsParseError
from kvguard.engines.vllm.metrics import VLLMPrometheusParser


class VLLMHttpCollector:
    """HTTP client for collecting metrics and health from a live vLLM instance."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        metrics_path: str = "/metrics",
        health_path: str = "/health",
        timeout: float = 5.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.metrics_url = f"{self.base_url}{metrics_path}"
        self.health_url = f"{self.base_url}{health_path}"
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def check_health(self) -> bool:
        """Query vLLM health endpoint."""
        client = await self.get_client()
        try:
            resp = await client.get(self.health_url)
            return resp.status_code == 200
        except Exception:
            return False

    async def fetch_metrics(self) -> Dict[str, float]:
        """Fetch and parse /metrics from vLLM."""
        client = await self.get_client()
        try:
            resp = await client.get(self.metrics_url)
            if resp.status_code != 200:
                raise EngineMetricsParseError(
                    f"vLLM metrics returned HTTP {resp.status_code}",
                    {"status_code": resp.status_code, "body": resp.text[:200]},
                )
            return VLLMPrometheusParser.parse_metrics_text(resp.text)
        except httpx.RequestError as exc:
            raise EngineConnectionError(
                f"Failed to connect to vLLM at {self.metrics_url}: {exc}",
                {"url": self.metrics_url},
            ) from exc
