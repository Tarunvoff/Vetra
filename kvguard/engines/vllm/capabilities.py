"""vLLM engine capability detection and documentation."""

from kvguard.core.enums import EngineType, FeatureStatus
from kvguard.core.models import EngineCapabilities


def get_vllm_capabilities(version: str = "0.4.x+") -> EngineCapabilities:
    """Return explicit capabilities for vLLM based on detected version."""
    return EngineCapabilities(
        engine_type=EngineType.VLLM,
        version=version,
        telemetry=True,
        request_metrics=True,
        block_metadata=False,  # vLLM internal block allocator is not exposed over HTTP
        direct_kv_control=False,  # Direct mutation unsupported over standard REST API
        offload=False,  # CPU swap handled internally by vLLM scheduler, not externally callable
        prefetch=False,
        eviction=False,
        quantization=False,
        remote_kv=False,
        semantic_reuse=False,
        status=FeatureStatus.IMPLEMENTED,
        notes="Real telemetry and metrics parsed from /metrics. Direct KV mutation is recommendation-only.",
    )
