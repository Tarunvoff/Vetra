"""Adaptive KV quantization strategy and simulation."""

from typing import Any, Dict, Optional
from kvguard.core.enums import QuantizationPrecision
from kvguard.core.models import KVBlockStats


class QuantizationStrategy:
    """Strategy selector and impact simulator for KV cache quantization."""

    def choose_precision(
        self, block: KVBlockStats, context: Optional[Dict[str, Any]] = None
    ) -> QuantizationPrecision:
        """Phase 1 returns NONE as real quantization is unsupported in baseline vLLM."""
        return QuantizationPrecision.NONE

    def simulate_quantization_impact(
        self,
        block: KVBlockStats,
        target_precision: QuantizationPrecision,
    ) -> Dict[str, Any]:
        """Estimate memory savings, latency impact, and perplexity risk for candidate precisions."""
        current_bytes = block.gpu_memory_bytes or block.cpu_memory_bytes or 131072
        compression_ratio = {
            QuantizationPrecision.NONE: 1.0,
            QuantizationPrecision.FP16: 1.0,
            QuantizationPrecision.BF16: 1.0,
            QuantizationPrecision.INT8: 0.5,
            QuantizationPrecision.INT4: 0.25,
        }.get(target_precision, 1.0)

        new_bytes = int(current_bytes * compression_ratio)
        saved_bytes = current_bytes - new_bytes

        quality_risk = {
            QuantizationPrecision.NONE: "LOW",
            QuantizationPrecision.FP16: "LOW",
            QuantizationPrecision.BF16: "LOW",
            QuantizationPrecision.INT8: "MEDIUM",
            QuantizationPrecision.INT4: "HIGH",
        }.get(target_precision, "LOW")

        return {
            "block_id": block.block_id,
            "target_precision": target_precision.value,
            "original_bytes": current_bytes,
            "quantized_bytes": new_bytes,
            "memory_saved_bytes": saved_bytes,
            "expected_latency_delta_ms": 2.5 if target_precision == QuantizationPrecision.INT4 else 0.5,
            "quality_risk": quality_risk,
            "is_simulation": True,
        }
