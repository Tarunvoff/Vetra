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
- `kvguard_gpu_memory_bytes`
- `kvguard_kv_memory_bytes`
- `kvguard_cache_hit_rate`
- `kvguard_cache_miss_rate`
- `kvguard_recommendations_total`
- `kvguard_estimated_memory_saved_bytes`
- `kvguard_estimated_cost_savings`
