"""Prometheus metric line parsing for vLLM telemetry."""

from __future__ import annotations

import re
from typing import Dict, Optional


class VLLMPrometheusParser:
    """Parser for vLLM /metrics exposition output."""

    # Matches Prometheus metric lines: name{labels} value or name value
    METRIC_LINE_REGEX = re.compile(
        r"^(?P<name>[a-zA-Z_:][a-zA-Z0-9_:]*)"
        r"(?:\{(?P<labels>[^\}]*)\})?"
        r"\s+(?P<value>[+-]?(?:[0-9]*[.])?[0-9]+(?:[eE][+-]?[0-9]+)?)"
    )

    @classmethod
    def parse_metrics_text(cls, text: str) -> Dict[str, float]:
        """Parse raw Prometheus text into key-value metric dictionary."""
        metrics: Dict[str, float] = {}

        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            match = cls.METRIC_LINE_REGEX.match(line)
            if match:
                name = match.group("name")
                val_str = match.group("value")
                try:
                    metrics[name] = float(val_str)
                except ValueError:
                    continue

        return metrics

    @staticmethod
    def extract_gpu_cache_usage(metrics: Dict[str, float]) -> Optional[float]:
        """Extract GPU cache usage factor [0.0, 1.0]."""
        # Supports standard vllm metric names across versions
        for key in [
            "vllm:gpu_cache_usage_factor",
            "vllm_gpu_cache_usage_factor",
            "vllm:num_gpu_blocks_used",
        ]:
            if key in metrics:
                val = metrics[key]
                return val if val <= 1.0 else min(1.0, val / 1000.0)
        return None

    @staticmethod
    def extract_cpu_cache_usage(metrics: Dict[str, float]) -> Optional[float]:
        """Extract CPU cache usage factor [0.0, 1.0]."""
        for key in [
            "vllm:cpu_cache_usage_factor",
            "vllm_cpu_cache_usage_factor",
            "vllm:num_cpu_blocks_used",
        ]:
            if key in metrics:
                val = metrics[key]
                return val if val <= 1.0 else min(1.0, val / 1000.0)
        return None

    @staticmethod
    def extract_prefix_cache_hit_rate(metrics: Dict[str, float]) -> Optional[float]:
        """Extract prefix cache hit rate from vLLM."""
        for key in [
            "vllm:prefix_cache_hit_rate",
            "vllm_prefix_cache_hit_rate",
            "vllm:gpu_prefix_cache_hit_rate",
        ]:
            if key in metrics:
                return max(0.0, min(1.0, metrics[key]))

        # Calculate from query vs hit counters if available
        hits = metrics.get("vllm:prefix_cache_hits_total", 0.0)
        queries = metrics.get("vllm:prefix_cache_queries_total", 0.0)
        if queries > 0:
            return max(0.0, min(1.0, hits / queries))

        return None
