"""Offloading bandwidth and latency impact estimation."""

from typing import Dict
from kvguard.core.models import KVBlockStats


class OffloadingOptimizer:
    """Estimates the bandwidth and latency overhead of offloading KV cache to host memory."""

    @staticmethod
    def estimate_offload_impact(block: KVBlockStats, pcie_bandwidth_gbps: float = 32.0) -> Dict[str, float]:
        bytes_to_transfer = block.gpu_memory_bytes or 131072
        transfer_seconds = bytes_to_transfer / (pcie_bandwidth_gbps * (1024 ** 3))
        return {
            "bytes_transferred": float(bytes_to_transfer),
            "estimated_latency_ms": transfer_seconds * 1000.0,
            "gpu_memory_released_bytes": float(bytes_to_transfer),
        }
