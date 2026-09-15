"""KV Cache block computations and memory sizing."""

from __future__ import annotations

import math
from kvguard.core.enums import CacheLocation, QuantizationPrecision
from kvguard.core.models import KVBlockStats


def calculate_kv_block_bytes(
    token_count: int = 16,
    num_layers: int = 32,
    num_kv_heads: int = 8,
    head_dim: int = 128,
    precision: QuantizationPrecision = QuantizationPrecision.FP16,
) -> int:
    """Calculate physical byte size of a KV cache block across all attention layers.

    Formula: 2 (K + V) * num_layers * num_kv_heads * head_dim * bytes_per_element * token_count
    """
    bytes_per_elem = {
        QuantizationPrecision.FP16: 2.0,
        QuantizationPrecision.BF16: 2.0,
        QuantizationPrecision.INT8: 1.0,
        QuantizationPrecision.INT4: 0.5,
        QuantizationPrecision.NONE: 2.0,
    }.get(precision, 2.0)

    total_elements = 2 * num_layers * num_kv_heads * head_dim * token_count
    return int(math.ceil(total_elements * bytes_per_elem))


def create_sample_block(
    block_id: str,
    tenant_id: str = "default",
    session_id: str = "session_1",
    token_count: int = 16,
    importance: float = 0.5,
) -> KVBlockStats:
    """Utility helper to instantiate a populated KVBlockStats object."""
    mem_bytes = calculate_kv_block_bytes(token_count=token_count)
    return KVBlockStats(
        block_id=block_id,
        tenant_id=tenant_id,
        session_id=session_id,
        token_count=token_count,
        gpu_memory_bytes=mem_bytes,
        cpu_memory_bytes=0,
        location=CacheLocation.GPU,
        importance_score=importance,
    )
