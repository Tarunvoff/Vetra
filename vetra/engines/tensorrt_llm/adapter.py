"""TensorRT-LLM engine adapter interface stub (Phase 2+)."""

from typing import Any, Dict, List
from vetra.core.enums import EngineType, FeatureStatus
from vetra.core.models import EngineCapabilities, GPUStats, KVBlockStats, RequestStats, UnifiedDecision
from vetra.engines.base import BaseInferenceEngineAdapter


class TensorRTLLMAdapter(BaseInferenceEngineAdapter):
    """Stub adapter for NVIDIA TensorRT-LLM backend."""

    def __init__(self, base_url: str = "http://localhost:8001", timeout: float = 5.0) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._capabilities = EngineCapabilities(
            engine_type=EngineType.TENSORRT_LLM,
            version="stub",
            telemetry=False,
            request_metrics=False,
            block_metadata=False,
            direct_kv_control=False,
            status=FeatureStatus.STUB,
            notes="Planned NVIDIA TensorRT-LLM C++ runtime adapter.",
        )

    async def get_engine_info(self) -> Dict[str, Any]:
        return {
            "engine": EngineType.TENSORRT_LLM.value,
            "status": "STUB",
            "message": "TensorRT-LLM adapter is planned for future release.",
        }

    async def get_gpu_stats(self) -> GPUStats:
        return GPUStats(device_name="TensorRT-LLM (Stub)")

    async def get_cache_stats(self) -> Dict[str, Any]:
        return {"status": "STUB", "message": "TensorRT-LLM cache stats not implemented."}

    async def get_request_stats(self) -> List[RequestStats]:
        return []

    def get_capabilities(self) -> EngineCapabilities:
        return self._capabilities

    async def get_block_stats(self) -> List[KVBlockStats]:
        return []
