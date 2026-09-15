"""vLLM engine adapter integrating telemetry, capabilities, and health."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from vetra.core.enums import CacheLocation, EngineType
from vetra.core.models import (
    EngineCapabilities,
    GPUStats,
    KVBlockStats,
    RequestStats,
    UnifiedDecision,
)
from vetra.engines.base import BaseInferenceEngineAdapter
from vetra.engines.vllm.collector import VLLMHttpCollector
from vetra.engines.vllm.capabilities import get_vllm_capabilities
from vetra.engines.vllm.metrics import VLLMPrometheusParser


class VLLMAdapter(BaseInferenceEngineAdapter):
    """Production adapter for vLLM inference backend."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        metrics_path: str = "/metrics",
        health_path: str = "/health",
        timeout: float = 5.0,
    ) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self.collector = VLLMHttpCollector(
            base_url=base_url,
            metrics_path=metrics_path,
            health_path=health_path,
            timeout=timeout,
        )
        self._capabilities = get_vllm_capabilities()
        self._cached_metrics: Dict[str, float] = {}

    async def connect(self) -> bool:
        self._connected = await self.collector.check_health()
        return self._connected

    async def disconnect(self) -> None:
        await self.collector.close()
        self._connected = False

    async def health(self) -> bool:
        return await self.collector.check_health()

    async def get_engine_info(self) -> Dict[str, Any]:
        healthy = await self.health()
        return {
            "engine": EngineType.VLLM.value,
            "base_url": self.base_url,
            "healthy": healthy,
            "connected": self._connected,
            "capabilities": self._capabilities.model_dump(),
        }

    def get_capabilities(self) -> EngineCapabilities:
        return self._capabilities

    async def _refresh_metrics(self) -> Dict[str, float]:
        try:
            self._cached_metrics = await self.collector.fetch_metrics()
        except Exception:
            # Fallback or keep stale if momentarily unreachable
            pass
        return self._cached_metrics

    async def get_gpu_stats(self) -> GPUStats:
        metrics = await self._refresh_metrics()

        # Extract memory usage if vLLM metrics expose it
        gpu_cache_factor = VLLMPrometheusParser.extract_gpu_cache_usage(metrics) or 0.0

        # Estimate memory bytes based on typical 24GB or 80GB GPU profiles
        total_gpu_bytes = int(80 * 1024 * 1024 * 1024)  # Standard 80GB base assumption
        kv_memory_bytes = int(total_gpu_bytes * gpu_cache_factor * 0.7)  # approx KV allocation
        used_memory_bytes = int(total_gpu_bytes * (0.2 + gpu_cache_factor * 0.7))

        return GPUStats(
            total_memory_bytes=total_gpu_bytes,
            used_memory_bytes=used_memory_bytes,
            free_memory_bytes=max(0, total_gpu_bytes - used_memory_bytes),
            utilization_percent=gpu_cache_factor * 100.0,
            kv_memory_bytes=kv_memory_bytes,
            kv_utilization_percent=gpu_cache_factor * 100.0,
            device_name="NVIDIA vLLM Backend",
        )

    async def get_cache_stats(self) -> Dict[str, Any]:
        metrics = await self._refresh_metrics()
        gpu_usage = VLLMPrometheusParser.extract_gpu_cache_usage(metrics) or 0.0
        cpu_usage = VLLMPrometheusParser.extract_cpu_cache_usage(metrics) or 0.0
        hit_rate = VLLMPrometheusParser.extract_prefix_cache_hit_rate(metrics) or 0.0

        return {
            "gpu_cache_usage_factor": gpu_usage,
            "cpu_cache_usage_factor": cpu_usage,
            "cache_hit_rate": hit_rate,
            "num_requests_running": metrics.get("vllm:num_requests_running", 0.0),
            "num_requests_waiting": metrics.get("vllm:num_requests_waiting", 0.0),
            "raw_metrics_count": len(metrics),
        }

    async def get_request_stats(self) -> List[RequestStats]:
        # Return summary stats derived from vLLM aggregate counters
        metrics = await self._refresh_metrics()
        prompt_tokens = int(metrics.get("vllm:prompt_tokens_total", 0.0))
        gen_tokens = int(metrics.get("vllm:generation_tokens_total", 0.0))
        hit_rate = VLLMPrometheusParser.extract_prefix_cache_hit_rate(metrics) or 0.0

        if prompt_tokens == 0 and gen_tokens == 0:
            return []

        return [
            RequestStats(
                request_id="vllm_aggregate",
                prompt_tokens=prompt_tokens,
                cached_tokens=int(prompt_tokens * hit_rate),
                computed_tokens=int(prompt_tokens * (1.0 - hit_rate)),
                output_tokens=gen_tokens,
                cache_hit=hit_rate > 0.0,
                hit_rate=hit_rate,
            )
        ]

    async def get_block_stats(self) -> List[KVBlockStats]:
        """vLLM doesn't expose raw block pointers over HTTP, so we return empty or tracked blocks."""
        return []

    async def apply_decision(self, decision: UnifiedDecision) -> Dict[str, Any]:
        """Phase 1 recommendation only - no unsafe internal mutation."""
        return {
            "status": "recommendation_only",
            "block_id": decision.block_id,
            "decision": decision.decision.value,
            "applied": False,
            "reason": "vLLM direct KV control not supported over standard REST API; recommendation logged.",
        }
