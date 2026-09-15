"""Simulated inference engine adapter allowing full offline execution without GPU or vLLM."""

from __future__ import annotations

import random
from typing import Any, Dict, List
from vetra.core.enums import EngineType, FeatureStatus
from vetra.core.models import (
    EngineCapabilities,
    GPUStats,
    KVBlockStats,
    RequestStats,
    UnifiedDecision,
)
from vetra.engines.base import BaseInferenceEngineAdapter
from vetra.simulation.state import SimulatedGPU, SimulatedKVCache
from vetra.simulation.workload import SimulatedRequest


class SimulatedEngineAdapter(BaseInferenceEngineAdapter):
    """Simulated inference engine adapter generating realistic telemetry and block states."""

    def __init__(self, base_utilization: float = 0.72) -> None:
        super().__init__(base_url="http://localhost:8000/simulated")
        self.gpu = SimulatedGPU(base_utilization=base_utilization)
        self.cache = SimulatedKVCache()
        self._capabilities = EngineCapabilities(
            engine_type=EngineType.SIMULATED,
            version="sim-0.1.0",
            telemetry=True,
            request_metrics=True,
            block_metadata=True,
            direct_kv_control=False,
            offload=False,
            prefetch=False,
            eviction=False,
            quantization=False,
            remote_kv=False,
            semantic_reuse=False,
            status=FeatureStatus.SIMULATED,
            notes="Offline simulation environment for testing and demonstrations.",
        )

    async def connect(self) -> bool:
        self._connected = True
        return True

    async def disconnect(self) -> None:
        self._connected = False

    async def health(self) -> bool:
        return True

    async def get_engine_info(self) -> Dict[str, Any]:
        return {
            "engine": EngineType.SIMULATED.value,
            "status": "SIMULATED",
            "connected": True,
            "mode": "offline_simulation",
            "capabilities": self._capabilities.model_dump(),
        }

    def get_capabilities(self) -> EngineCapabilities:
        return self._capabilities

    async def get_gpu_stats(self) -> GPUStats:
        return self.gpu.step()

    async def get_cache_stats(self) -> Dict[str, Any]:
        gpu_stats = await self.get_gpu_stats()
        hit_rate = 0.62 + (random.random() - 0.5) * 0.1
        return {
            "gpu_cache_usage_factor": gpu_stats.memory_pressure,
            "cpu_cache_usage_factor": 0.25,
            "cache_hit_rate": round(max(0.1, min(0.95, hit_rate)), 3),
            "num_requests_running": random.randint(4, 16),
            "num_requests_waiting": random.randint(0, 3),
            "is_simulation": True,
        }

    async def get_request_stats(self) -> List[RequestStats]:
        return SimulatedRequest.generate_batch(count=5)

    async def get_block_stats(self) -> List[KVBlockStats]:
        return list(self.cache.blocks.values())

    async def apply_decision(self, decision: UnifiedDecision) -> Dict[str, Any]:
        return {
            "status": "simulated_success",
            "block_id": decision.block_id,
            "decision": decision.decision.value,
            "applied": True,
            "is_simulation": True,
            "reason": f"Simulated execution of {decision.decision.value} on block {decision.block_id}",
        }
