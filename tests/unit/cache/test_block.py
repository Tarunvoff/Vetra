from vetra.cache.block import calculate_kv_block_bytes
from vetra.core.enums import QuantizationPrecision


def test_calculate_kv_block_bytes():
    # 2 * 32 layers * 8 heads * 128 dim * 2 bytes * 16 tokens = 2,097,152 bytes = 2MB
    fp16_bytes = calculate_kv_block_bytes(
        token_count=16, num_layers=32, num_kv_heads=8, head_dim=128, precision=QuantizationPrecision.FP16
    )
    int8_bytes = calculate_kv_block_bytes(
        token_count=16, num_layers=32, num_kv_heads=8, head_dim=128, precision=QuantizationPrecision.INT8
    )

    assert fp16_bytes > 0
    assert int8_bytes == fp16_bytes // 2
