"""Prometheus client exporter registering Vetra control plane metrics."""

from __future__ import annotations

from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest

# Dedicated Prometheus registry for Vetra
vetra_metrics_registry = CollectorRegistry(auto_describe=True)

# Gauges
GPU_MEMORY_BYTES = Gauge(
    "vetra_gpu_memory_bytes",
    "Total GPU memory used in bytes",
    registry=vetra_metrics_registry,
)

KV_MEMORY_BYTES = Gauge(
    "vetra_kv_memory_bytes",
    "Total KV cache memory allocated in bytes",
    registry=vetra_metrics_registry,
)

CACHE_HIT_RATE = Gauge(
    "vetra_cache_hit_rate",
    "Current KV cache hit rate [0.0 - 1.0]",
    registry=vetra_metrics_registry,
)

CACHE_MISS_RATE = Gauge(
    "vetra_cache_miss_rate",
    "Current KV cache miss rate [0.0 - 1.0]",
    registry=vetra_metrics_registry,
)

ESTIMATED_MEMORY_SAVED_BYTES = Gauge(
    "vetra_estimated_memory_saved_bytes",
    "Estimated GPU memory saved by Vetra policy recommendations",
    registry=vetra_metrics_registry,
)

ESTIMATED_COST_SAVINGS_USD = Gauge(
    "vetra_estimated_cost_savings",
    "Estimated hourly infrastructure cost savings in USD",
    registry=vetra_metrics_registry,
)

# Counters
RECOMMENDATIONS_TOTAL = Counter(
    "vetra_recommendations_total",
    "Total policy recommendations generated",
    ["decision_type"],
    registry=vetra_metrics_registry,
)

CACHE_EVENTS_TOTAL = Counter(
    "vetra_cache_events_total",
    "Total cache events processed",
    ["event_type"],
    registry=vetra_metrics_registry,
)


def export_prometheus_metrics() -> bytes:
    """Render metrics in standard Prometheus exposition format."""
    return generate_latest(vetra_metrics_registry)
