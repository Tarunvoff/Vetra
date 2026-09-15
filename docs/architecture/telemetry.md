# Telemetry Architecture

## Polling & Normalization
```
vLLM / Engine (/metrics)
       │
       ▼
VLLMHttpCollector
       │
       ▼
VLLMPrometheusParser
       │
       ▼
TelemetryCollector
       │
       ▼
TelemetryAggregator & Prometheus Client Exporter (/metrics)
```

Exposed Metrics:
- `vetra_gpu_memory_bytes`
- `vetra_kv_memory_bytes`
- `vetra_cache_hit_rate`
- `vetra_cache_miss_rate`
- `vetra_recommendations_total`
- `vetra_estimated_memory_saved_bytes`
- `vetra_estimated_cost_savings`
