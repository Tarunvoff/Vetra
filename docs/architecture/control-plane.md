# Control Plane Architecture

The KVGuard Control Plane provides asynchronous orchestration above the LLM inference tier.

## Key Subsystems
1. **Telemetry Collector**: Periodically ingests engine metrics without degrading latency.
2. **Scoring Engine**: Evaluates normalized utility scores for logical KV blocks.
3. **Policy Engine**: Decides retention, CPU offload, prefetch, and eviction.
4. **Metadata Repository**: Stores lightweight block headers and access statistics in Redis.
5. **FastAPI & SDK**: Exposes REST and programmatic control.
