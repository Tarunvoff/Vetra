import pytest
from vetra.engines.vllm.adapter import VLLMAdapter
from vetra.engines.vllm.metrics import VLLMPrometheusParser


SAMPLE_VLLM_METRICS = """
# HELP vllm:gpu_cache_usage_factor GPU KV-cache usage.
# TYPE vllm:gpu_cache_usage_factor gauge
vllm:gpu_cache_usage_factor 0.82
# HELP vllm:cpu_cache_usage_factor CPU KV-cache usage.
# TYPE vllm:cpu_cache_usage_factor gauge
vllm:cpu_cache_usage_factor 0.15
# HELP vllm:prefix_cache_hit_rate Prefix cache hit rate.
# TYPE vllm:prefix_cache_hit_rate gauge
vllm:prefix_cache_hit_rate 0.654
# HELP vllm:num_requests_running Number of running requests.
# TYPE vllm:num_requests_running gauge
vllm:num_requests_running 8.0
"""


def test_vllm_prometheus_parser():
    parsed = VLLMPrometheusParser.parse_metrics_text(SAMPLE_VLLM_METRICS)
    assert parsed["vllm:gpu_cache_usage_factor"] == 0.82
    assert parsed["vllm:cpu_cache_usage_factor"] == 0.15
    assert parsed["vllm:prefix_cache_hit_rate"] == 0.654
    assert parsed["vllm:num_requests_running"] == 8.0

    gpu_usage = VLLMPrometheusParser.extract_gpu_cache_usage(parsed)
    assert gpu_usage == 0.82

    hit_rate = VLLMPrometheusParser.extract_prefix_cache_hit_rate(parsed)
    assert hit_rate == 0.654
