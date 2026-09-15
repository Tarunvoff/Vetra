"""SGLang engine adapter interface stub (Phase 2+)."""

from typing import Any, Dict, List
from vetra.core.enums import EngineType, FeatureStatus
from vetra.core.models import EngineCapabilities, GPUStats, KVBlockStats, RequestStats, UnifiedDecision
from vetra.engines.base import BaseInferenceEngineAdapter


class SGLangAdapter(BaseInferenceEngineAdapter):
    """Stub adapter for SGLang inference backend (RadixAttention integration planned)."""

    def __init__(self, base_url: str = "http://localhost:30000", timeout: float = 5.0) -> None:
        super().__init__(base_url=base_url, timeout=timeout)
        self._capabilities = EngineCapabilities(
            engine_type=EngineType.SGLANG,
            version="stub",
            telemetry=False,
            request_metrics=False,
            block_metadata=False,
            direct_kv_control=False,
            status=FeatureStatus.STUB,
            notes="Planned SGLang RadixAttention control-plane adapter.",
        )

    async def get_engine_info(self) -> Dict[str, Any]:
        return {
            "engine": EngineType.SGLANG.value,
            "status": "STUB",
            "message": "SGLang adapter is planned for future release.",
        }

    async def get_gpu_stats(self) -> GPUStats:
        return GPUStats(device_name="SGLang (Stub)")

    async def get_cache_stats(self) -> Dict[str, Any]:
        return {"status": "STUB", "message": "SGLang cache stats not implemented."}

    async def get_request_stats(self) -> List[RequestStats]:
        return []

    def get_capabilities(self) -> EngineCapabilities:
        return self._capabilities

    async def get_block_stats(self) -> List[KVBlockStats]:
        return []
