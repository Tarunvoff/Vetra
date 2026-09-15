"""GPU monitor wrapper supporting both physical NVML inspection and engine fallbacks."""

from __future__ import annotations

import logging
from typing import Optional
from kvguard.core.models import GPUStats

logger = logging.getLogger("kvguard.telemetry.gpu")


class GPUMonitor:
    """Monitor for polling GPU memory and compute metrics."""

    def __init__(self, device_id: int = 0) -> None:
        self.device_id = device_id
        self._nvml_available = False
        self._init_nvml()

    def _init_nvml(self) -> None:
        try:
            import pynvml  # Optional hardware dependency
            pynvml.nvmlInit()
            self._nvml_available = True
            logger.info("NVML initialized successfully.")
        except Exception:
            self._nvml_available = False

    def query_gpu_stats(self) -> Optional[GPUStats]:
        """Query physical GPU via NVML if installed and available."""
        if not self._nvml_available:
            return None

        try:
            import pynvml
            handle = pynvml.nvmlDeviceGetHandleByIndex(self.device_id)
            mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)
            name = pynvml.nvmlDeviceGetName(handle)
            if isinstance(name, bytes):
                name = name.decode("utf-8")

            return GPUStats(
                total_memory_bytes=mem_info.total,
                used_memory_bytes=mem_info.used,
                free_memory_bytes=mem_info.free,
                utilization_percent=float(util.gpu),
                kv_memory_bytes=0,
                kv_utilization_percent=0.0,
                device_name=name,
            )
        except Exception as e:
            logger.debug(f"NVML query error: {e}")
            return None
